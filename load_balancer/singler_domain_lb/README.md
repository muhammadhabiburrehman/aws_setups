# AWS Load Balancer & Certificate Manager Guide

## Table of Contents
1. [What is a Load Balancer?](#what-is-a-load-balancer)
2. [Types of Load Balancers in AWS](#types-of-load-balancers-in-aws)
3. [Key Terminologies](#key-terminologies)
4. [Creating Load Balancer via Console](#creating-load-balancer-via-console)
5. [AWS Certificate Manager (ACM)](#aws-certificate-manager-acm)
6. [Domain Setup with Load Balancer](#domain-setup-with-load-balancer)
7. [Complete Flow](#complete-flow)

---

## What is a Load Balancer?

A Load Balancer is a service that **distributes incoming network traffic** across multiple targets (like EC2 instances, containers, or IP addresses) to ensure:
- **High availability** - if one server fails, traffic routes to healthy servers
- **Improved performance** - distributes load to prevent any single server from being overwhelmed
- **Scalability** - can easily add/remove servers as needed

---

## Types of Load Balancers in AWS

### 1. **Application Load Balancer (ALB)**
- **Layer 7** (HTTP/HTTPS)
- Best for web applications
- Supports path-based and host-based routing
- Can route to different target groups based on URL paths

### 2. **Network Load Balancer (NLB)**
- **Layer 4** (TCP/UDP)
- Ultra-high performance, low latency
- Handles millions of requests per second
- Best for gaming, IoT, or high-throughput applications

### 3. **Gateway Load Balancer (GWLB)**
- **Layer 3** (Network layer)
- Used for deploying, scaling, and managing third-party virtual appliances
- Common for firewalls, intrusion detection systems

### 4. **Classic Load Balancer (CLB)**
- **Legacy** - operates at both Layer 4 and Layer 7
- Not recommended for new applications
- Being phased out in favor of ALB/NLB

---

## Key Terminologies

### 🎯 **Target**
- Individual resource that receives traffic (EC2 instance, container, IP address)
- Can be in different Availability Zones
- Must be healthy to receive traffic

### 👥 **Target Group**
- Collection of targets that the load balancer routes requests to
- You define health check settings at target group level
- Can have multiple target groups per load balancer

### 👂 **Listener**
- Process that **checks for connection requests** using protocol and port you configure
- Rules determine how the load balancer routes requests to targets
- Example: HTTP listener on port 80, HTTPS listener on port 443

### 📋 **Listener Rules**
- Define **how to route incoming requests** to target groups
- Based on conditions like:
  - Host header (`api.example.com` vs `www.example.com`)
  - Path patterns (`/api/*` vs `/images/*`)
  - HTTP methods (GET, POST, etc.)
  - Source IP addresses

---

## Creating Load Balancer via Console

### Prerequisites: Create EC2 Instances First

**⚠️ Important**: Before creating a load balancer, you need targets to route traffic to!

#### Create EC2 Instances:

1. **Launch EC2 Instances**
   - Go to AWS Console → EC2 → Instances
   - Click "Launch Instance"
   - **Recommended**: Create 2 or more instances for high availability

2. **Instance Configuration**
   - **AMI**: Choose appropriate AMI (e.g., Amazon Linux 2)
   - **Instance Type**: t2.micro or as per your needs
   - **Key Pair**: Select or create key pair for SSH access
   - **Security Group**: 
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
     - Allow HTTPS (port 443) from anywhere if using SSL

3. **Deploy Your Application**
   - SSH into each instance
   - Install and configure your web server (Apache, Nginx, etc.)
   - Deploy your application code
   - **Test**: Ensure your app is accessible via instance public IP

4. **Multiple Availability Zones (Recommended)**
   - Create instances in different AZs for high availability
   - Example: 1 instance in us-east-1a, 1 instance in us-east-1b

### Step-by-Step Load Balancer Creation:

1. **Navigate to EC2 Console**
   - Go to AWS Console → EC2 → Load Balancers

2. **Create Load Balancer**
   - Click "Create Load Balancer"
   - Choose type (usually Application Load Balancer for web apps)

3. **Basic Configuration**
   - **Name**: Give your load balancer a name
   - **Scheme**: Internet-facing or Internal
   - **IP Address Type**: IPv4 or Dual stack

4. **Network Mapping**
   - **VPC**: Select your VPC
   - **Availability Zones**: Select at least 2 AZs
   - **Subnets**: Choose public subnets for internet-facing LB

5. **Security Groups**
   - Create or select security group
   - Allow inbound traffic on ports 80 (HTTP) and 443 (HTTPS)

6. **Configure Listeners**
   - **HTTP Listener**: Port 80 → Forward to target group
   - **HTTPS Listener**: Port 443 → Forward to target group (requires SSL certificate)

7. **Create Target Group**
   - **Target Type**: Instances, IP addresses, or Lambda functions
   - **Protocol**: HTTP/HTTPS
   - **Port**: Application port (usually 80 or 8080)
   - **Health Check**: Configure path and settings

8. **Register Targets**
   - Select EC2 instances or other targets
   - Add to target group

9. **Review and Create**

---

## AWS Certificate Manager (ACM)

### What is ACM?
AWS Certificate Manager is a service that lets you easily **provision, manage, and deploy SSL/TLS certificates** for use with AWS services.

### Key Benefits:
- **Free SSL certificates** for AWS services
- **Automatic renewal** - no manual certificate management
- **Easy integration** with Load Balancers, CloudFront, API Gateway

### Steps to Use ACM:

1. **Request Certificate**
   - Go to Certificate Manager in AWS Console
   - Click "Request a certificate"
   - Choose "Request a public certificate"

2. **Domain Configuration**
   - Enter your domain name (e.g., `app.yourdomain.com`)
   - Add additional domains if needed (wildcards supported: `*.yourdomain.com`)

3. **Validation Methods**
   - **DNS Validation** (recommended): Add CNAME record to your DNS
   - **Email Validation**: Receive validation email

4. **DNS Validation Process**
   - ACM provides CNAME record details
   - Add this record to your domain's DNS settings
   - Wait for validation (usually 5-10 minutes)

5. **Certificate Issued**
   - Once validated, certificate status becomes "Issued"
   - Can now be used with AWS services

---

## Domain Setup with Load Balancer

### Complete Process:

1. **Get Load Balancer DNS Name**
   - After creating LB, copy the DNS name
   - Example: `my-app-lb-1234567890.us-east-1.elb.amazonaws.com`

2. **Update DNS Records**
   - Go to your domain registrar or DNS provider
   - Create/update DNS record:
     - **Type**: CNAME (or A record with alias if using Route 53)
     - **Name**: Your subdomain (e.g., `app`)
     - **Value**: Load Balancer DNS name

3. **Attach Certificate to Load Balancer**
   - Edit HTTPS listener on load balancer
   - Select your ACM certificate
   - Save changes

### Example DNS Configuration:
```
Type: CNAME
Name: app
Value: my-app-lb-1234567890.us-east-1.elb.amazonaws.com
TTL: 300
```

---

## Complete Flow

Here's how everything works together:

```
User visits app.yourdomain.com
           ↓
DNS resolves to Load Balancer
           ↓
Load Balancer receives request
           ↓
HTTPS Listener checks SSL certificate (ACM)
           ↓
Listener Rules determine routing
           ↓
Request forwarded to Target Group
           ↓
Target Group routes to healthy Target
           ↓
Target (EC2 instance) processes request
           ↓
Response sent back through same path
```

### Security Flow:
1. **SSL Termination**: Load Balancer handles SSL/TLS encryption using ACM certificate
2. **Security Groups**: Control traffic at LB and instance level
3. **Health Checks**: Ensure only healthy targets receive traffic

---


## Important Notes:
- Always use **at least 2 Availability Zones** for high availability
- **Health checks** are crucial - configure appropriate health check paths
- **Security groups** must allow traffic on listener ports
- **ACM certificates** are region-specific
- Use **Route 53** for better integration with AWS services

---

## Troubleshooting Common Issues

### Load Balancer Shows Unhealthy Targets:
- Check security groups on instances
- Verify health check path returns 200 OK
- Ensure application is running on correct port

### Certificate Not Working:
- Verify DNS validation is complete
- Check certificate is in same region as load balancer
- Ensure HTTPS listener is configured with certificate

### Domain Not Resolving:
- Verify DNS propagation (can take up to 48 hours)
- Check DNS record configuration
- Use tools like `nslookup` or `dig` to verify

---

*Author: Muhammad Habib*