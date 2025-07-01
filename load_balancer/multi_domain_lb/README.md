# Multi-Subdomain Load Balancer with Host-Based Routing

## Overview
This guide demonstrates how to set up **host-based routing** using AWS Application Load Balancer where different subdomains route to different EC2 instances. This is perfect for **microservices architecture** or **multi-tenant applications**.

## Architecture
```
Internet
    ↓
Application Load Balancer
    ↓
┌─────────────────┬─────────────────┐
│  app1.domain    │  app2.domain    │
│      ↓          │      ↓          │
│  Target Group 1 │  Target Group 2 │
│      ↓          │      ↓          │
│  EC2 Instance 1 │  EC2 Instance 2 │
└─────────────────┴─────────────────┘
```
---
```
app1.dockerconvert.xyz → Load Balancer → Target Group 1 → EC2 Instance 1
app2.dockerconvert.xyz → Load Balancer → Target Group 2 → EC2 Instance 2
```

---


## Infrastructure Components

### 1. EC2 Instances
- **Instance 1**: Serves content for `app1.dockerconvert.xyz`
- **Instance 2**: Serves content for `app2.dockerconvert.xyz`

### 2. Target Groups
- **Target Group 1**: Contains EC2 Instance 1
- **Target Group 2**: Contains EC2 Instance 2

### 3. Application Load Balancer
- Distributes incoming traffic based on domain name
- Handles both HTTP (port 80) and HTTPS (port 443) traffic

### 4. SSL Certificate (ACM)
- Single certificate covering multiple subdomains:
  - `app1.dockerconvert.xyz`
  - `app2.dockerconvert.xyz`


## What I Built

### Final Result:
- **app1.dockerconvert.xyz** → Shows output from Target 1 (Instance 1)
- **app2.dockerconvert.xyz** → Shows output from Target 2 (Instance 2)
- Both subdomains use **same Load Balancer** with different **Listener Rules**
- **HTTPS enabled** for both subdomains with single wildcard certificate

---

## Step-by-Step Implementation


### Step 1: Create EC2 Instances
1. Launch 2 EC2 instances in your preferred AWS region
2. Configure security groups to allow inbound traffic on required ports
3. Install and configure your applications on each instance
4. Test that applications are running correctly

```
#!/bin/bash
apt update -y
apt install -y nginx
echo "Hello from web-server-1" > /var/www/html/index.html
systemctl enable nginx
systemctl start nginx

```
**Note**: **Repeat this step for second EC2**

### Step 2: Create Target Groups
1. Navigate to EC2 Console → Target Groups
2. Create Target Group 1:
   - **Name**: `app1-targets`
   - **Protocol**: HTTP
   - **Port**: 80 (or your app port)
   - **VPC**: Select your VPC
   - **Health Check**: Configure appropriate health check path
3. Create Target Group 2:
   - **Name**: `app2-targets`
   - **Protocol**: HTTP
   - **Port**: 80 (or your app port)
   - **VPC**: Select your VPC
   - **Health Check**: Configure appropriate health check path
4. Register targets:
   - Add EC2 Instance 1 to Target Group 1
   - Add EC2 Instance 2 to Target Group 2

### Step 3: Request SSL Certificate
1. Navigate to AWS Certificate Manager (ACM)
2. Request a public certificate
3. Add domain names:
   - `app1.dockerconvert.xyz`
   - `app2.dockerconvert.xyz`
4. Choose DNS validation
5. Complete domain validation process
6. Wait for certificate status to become "Issued"

### Step 4: Create Application Load Balancer
1. Navigate to EC2 Console → Load Balancers
2. Create Application Load Balancer:
   - **Name**: `multi-domain-alb`
   - **Scheme**: Internet-facing
   - **IP address type**: IPv4
   - **VPC**: Select your VPC
   - **Availability Zones**: Select at least 2 AZs
   - **Security Groups**: Create/select appropriate security group


### Step 5: Configure HTTP Listener Rules

1. Go to Load Balancer → Listeners → HTTP:80
2. Click "View/edit rules"

#### Add Custom HTTP Rules:

**Rule 1 - app1.dockerconvert.xyz:**
```
Priority: 1
Conditions:
- Host header: app1.dockerconvert.xyz
Actions:
- Forward to: app1-target-group
```

**Rule 2 - app2.dockerconvert.xyz:**
```
Priority: 2
Conditions:
- Host header: app2.dockerconvert.xyz
Actions:
- Forward to: app2-target-group
```

**Rule 3 - Default Rule (Optional):**
```
Priority: 3 (lowest)
Conditions: Default (catches all other requests)
Actions:
- Return fixed response: 404 "Not Found"
```

### Step 6: Configure HTTPS Listener Rules

#### Add HTTPS Listener:
```
Protocol: HTTPS
Port: 443
SSL Certificate: Select your ACM certificate
Security Policy: ELBSecurityPolicy-TLS-1-2-2017-01
```

#### Add Same Rules for HTTPS:

**HTTPS Rule 1 - app1.dockerconvert.xyz:**
```
Priority: 1
Conditions:
- Host header: app1.dockerconvert.xyz
Actions:
- Forward to: app1-target-group
```

**HTTPS Rule 2 - app2.dockerconvert.xyz:**
```
Priority: 2
Conditions:
- Host header: app2.dockerconvert.xyz
Actions:
- Forward to: app2-target-group
```

**HTTPS Default Rule:**
```
Priority: 3
Conditions: Default
Actions:
- Return fixed response: 404 "Not Found"
```

### Step 7: Configure DNS Records

Update your DNS records to point to the ALB:
   - `app1.dockerconvert.xyz` → ALB DNS name (CNAME or A record)
   - `app2.dockerconvert.xyz` → ALB DNS name (CNAME or A record)

Add these CNAME records to your DNS provider:
```
Type: CNAME
Name: app1
Value: multi-app-load-balancer-xxxxxxxxx.us-east-1.elb.amazonaws.com
TTL: 300

Type: CNAME
Name: app2
Value: multi-app-load-balancer-xxxxxxxxx.us-east-1.elb.amazonaws.com
TTL: 300
```

---

## Testing
### HTTP Testing
```bash
curl -H "Host: app1.dockerconvert.xyz" http://your-alb-dns-name
curl -H "Host: app2.dockerconvert.xyz" http://your-alb-dns-name
```

### HTTPS Testing
```bash
curl https://app1.dockerconvert.xyz
curl https://app2.dockerconvert.xyz
```


### Browser Testing:
1. Visit `https://app1.dockerconvert.xyz` → Should show Instance 1 content
2. Visit `https://app2.dockerconvert.xyz` → Should show Instance 2 content

---
## Configuration Summary

### Current Setup
- **Domain**: dockerconvert.xyz
- **Subdomains**: 
  - app1.dockerconvert.xyz → EC2 Instance 1
  - app2.dockerconvert.xyz → EC2 Instance 2
- **Load Balancer**: Application Load Balancer with host-based routing
- **SSL**: Single ACM certificate covering both subdomains
- **Protocols**: HTTP (80) and HTTPS (443) listeners configured

### Traffic Flow
1. User visits app1.dockerconvert.xyz or app2.dockerconvert.xyz
2. DNS resolves to ALB
3. ALB receives request and checks host header
4. Based on host header, ALB forwards to appropriate target group
5. Target group routes to corresponding EC2 instance
6. Instance serves the response back through ALB to user

## Traffic Flow Diagram

```
User Request: https://app1.dockerconvert.xyz
                    ↓
DNS Resolution: Load Balancer IP
                    ↓
Load Balancer: Receives HTTPS request
                    ↓
SSL Termination: Using ACM certificate
                    ↓
HTTPS Listener: Port 443
                    ↓
Rule Evaluation: Host header = app1.dockerconvert.xyz
                    ↓
Match Found: Priority 1 rule
                    ↓
Forward to: app1-target-group
                    ↓
Target Selection: Instance 1 (healthy target)
                    ↓
Response: "Welcome to App1" content
```

---

## Security Considerations

### Security Groups
- **ALB Security Group**: Allow inbound traffic on ports 80 and 443 from 0.0.0.0/0
- **EC2 Security Group**: Allow inbound traffic from ALB security group on application port

### SSL/TLS
- ACM certificate provides automatic renewal
- ALB handles SSL termination
- Backend communication can be HTTP or HTTPS based on requirements

## Monitoring and Troubleshooting

### CloudWatch Metrics
- Monitor ALB metrics: RequestCount, TargetResponseTime, HTTPCode_Target_2XX_Count
- Monitor target group health status

### Health Checks
- Ensure target groups have appropriate health check configuration
- Verify targets are showing as "healthy" in target group

### Common Issues
1. **Targets showing unhealthy**:
   - Check security group rules
   - Verify application is running on correct port
   - Check health check path and response

2. **SSL certificate issues**:
   - Verify certificate status is "Issued"
   - Ensure domain validation is complete
   - Check that certificate covers all required domains

3. **Routing issues**:
   - Verify listener rules are configured correctly
   - Check rule priorities and conditions
   - Test with curl using Host header

## Cost Optimization

- Use appropriate EC2 instance types for your workload
- Consider using Auto Scaling Groups for better resource utilization
- Monitor ALB usage to ensure cost-effectiveness
- Use Reserved Instances or Savings Plans for predictable workloads

## Next Steps

- Implement Auto Scaling Groups for high availability
- Add CloudWatch alarms for monitoring
- Consider using AWS WAF for additional security
- Implement logging with ALB access logs
- Set up CI/CD pipeline for application deployments


## Resources

- [AWS Application Load Balancer Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)
- [AWS Certificate Manager Documentation](https://docs.aws.amazon.com/acm/)
- [Target Groups Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html)

---

**Note**: Replace `dockerconvert.xyz` with your actual domain name and adjust configuration parameters according to your specific requirements.