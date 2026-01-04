# AWS Infrastructure Architecture for Monolithic Matrimonial Application

**Status:** Accepted
**Cloud Provider:** aws
**Target Environments:** dev, staging, prod

## Summary

This Architecture Decision Record defines the infrastructure for a matrimonial application deployed on AWS. In strict adherence to mandatory user constraints, the application backend is architected and hosted using Virtual Machines (EC2) - Traditional monolithic deployment. The database layer utilizes Amazon RDS for PostgreSQL for all user profiles and matching data. Complex search requirements are handled via standard database queries, as a dedicated search engine is explicitly excluded. User-uploaded media (photos/videos) are configured to Serve via CloudFront CDN for performance. The frontend client is hosted using AWS Amplify Hosting. This architecture ensures compliance with all specified technical constraints while providing a robust, scalable foundation.

## Context

### Business Drivers

- Ensure high availability for user matching and profile viewing
- Deliver high-resolution media with low latency globally
- Maintain strict data privacy and isolation for user PII
- Enable independent deployment cycles for the frontend interface

### Technical Constraints

- Backend architecture must use Virtual Machines (EC2) - Traditional monolithic deployment
- Database engine must be Amazon RDS for PostgreSQL
- No dedicated search engine allowed; must use standard database queries
- Media handling must Serve via CloudFront CDN for performance
- Frontend hosting must use AWS Amplify Hosting

### Compliance Requirements

- GDPR data residency and processing standards
- Encryption at rest for all persistent data stores

## Decision

### Selected Approach

The solution adopts a Virtual Machines (EC2) - Traditional monolithic deployment architecture within a VPC. The application logic resides on EC2 instances behind an Application Load Balancer. To handle media efficiently, the system is designed to Serve via CloudFront CDN for performance. The database layer is consolidated on Amazon RDS for PostgreSQL.

### Key Services

#### Amazon EC2

**Purpose:** Host the backend application logic as a Virtual Machines (EC2) - Traditional monolithic deployment

**Configuration:** t3.medium instances in Auto Scaling Group, Amazon Linux 2023

#### Amazon RDS for PostgreSQL

**Purpose:** Primary relational database for user profiles and matching data

**Configuration:** db.t3.large, Multi-AZ for production, storage encryption enabled

#### Amazon CloudFront

**Purpose:** Content Delivery Network configured to Serve via CloudFront CDN for performance

**Configuration:** Price Class 100, Origin Access Control (OAC) for S3 origin

#### AWS Amplify Hosting

**Purpose:** Managed hosting service for the frontend client application

**Configuration:** Continuous deployment from Git repository, custom domain configuration

#### Application Load Balancer (ALB)

**Purpose:** Distribute HTTPS traffic to the EC2 monolithic instances

**Configuration:** Internet-facing, HTTP/2 enabled, sticky sessions if required

### Network Topology

A multi-AZ VPC architecture containing Public Subnets for ALB/NAT Gateways, Private Application Subnets for EC2 instances, and Private Database Subnets for RDS. Outbound internet access for private resources is routed through NAT Gateways.

### Security Boundaries

Network isolation is enforced via Security Groups. ALB accepts 443 from 0.0.0.0/0. EC2 accepts traffic only from ALB. RDS accepts traffic only from EC2. S3 media buckets are restricted to CloudFront OAC identity only.

## Alternatives Considered

### Containerized Microservices (ECS/EKS)

**Trade-offs:** Provides greater agility and resource packing but increases orchestration complexity.

**Rejection Reason:** Rejected because the requirement specifies Virtual Machines (EC2) - Traditional monolithic deployment.

### Dedicated Search Engine (OpenSearch)

**Trade-offs:** Offers superior full-text search capabilities but adds cost and infrastructure overhead.

**Rejection Reason:** Rejected because standard database queries are sufficient and mandated.

### Direct S3 Access for Media

**Trade-offs:** Simpler setup but higher latency and data transfer costs.

**Rejection Reason:** Rejected because the system must Serve via CloudFront CDN for performance.

## Implementation

### Terraform Modules

#### vpc-infrastructure

**Purpose:** Deploys VPC, subnets, route tables, IGW, and NAT Gateways

#### database-rds

**Purpose:** Deploys RDS PostgreSQL instance and subnet groups

**Dependencies:** vpc-infrastructure

#### backend-compute

**Purpose:** Deploys ALB, Launch Templates, ASG, and EC2 instances

**Dependencies:** vpc-infrastructure, database-rds

#### media-cdn

**Purpose:** Deploys S3 buckets and CloudFront distribution

#### frontend-amplify

**Purpose:** Deploys AWS Amplify app configuration

### Provider Configuration

AWS Provider configured with region constraints and default tags for cost allocation.

### State Management

Terraform state stored in S3 with versioning enabled and DynamoDB table for state locking.

### Deployment Order

1. vpc-infrastructure
2. database-rds
3. media-cdn
4. backend-compute
5. frontend-amplify

## Security

### IAM Strategy

Least-privilege IAM Roles for EC2 (Instance Profiles) to access specific S3 buckets. No hardcoded credentials. Separate roles for deployment pipelines.

### Network Security

Strict Security Group rules. WAF applied to ALB and CloudFront to mitigate common web attacks. Private subnets for all compute and database resources.

### Encryption

AES-256 encryption for data at rest (EBS, RDS, S3). TLS 1.2+ for all data in transit.

### Compliance Controls

- AWS Config rules for resource compliance
- CloudTrail logging for audit trails
- S3 Block Public Access enabled globally

## Risks

### Complex Query Performance

**Severity:** medium

**Mitigation:** Optimize PostgreSQL indexes and use Read Replicas since dedicated search is not allowed.

### Monolithic Scaling Limits

**Severity:** medium

**Mitigation:** Implement aggressive Auto Scaling policies based on CPU and Memory utilization.

### Single Region Dependency

**Severity:** low

**Mitigation:** Architecture is Multi-AZ, but cross-region DR would require additional configuration if needed.
