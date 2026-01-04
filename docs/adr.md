# Provisioning AWS EKS Infrastructure for Microservices

**Status:** Proposed
**Cloud Provider:** aws
**Target Environments:** dev, staging, prod

## Summary

This decision records the architectural strategy for deploying a scalable, production-grade Kubernetes environment using Amazon Elastic Kubernetes Service (EKS). The infrastructure will be provisioned entirely via Terraform to ensure consistency across development, staging, and production environments. The design prioritizes high availability by spanning three Availability Zones, security through strict network isolation and IAM Roles for Service Accounts (IRSA), and operational efficiency using Managed Node Groups. This foundation supports the organization's shift to a microservices architecture.

## Context

### Business Drivers

- Need for high availability and fault tolerance for critical business applications
- Requirement to accelerate deployment cycles through containerization
- Scalability requirements to handle fluctuating user traffic patterns

### Technical Constraints

- Infrastructure must be defined as code using Terraform for reproducibility
- Strict network isolation requirements between public and private workloads
- Requirement to minimize operational overhead of managing the Kubernetes control plane

### Compliance Requirements

- SOC2 Type II infrastructure controls
- Data residency requirements within specific AWS regions

## Decision

### Selected Approach

Deploy Amazon EKS with Managed Node Groups within a custom VPC architecture designed for container workloads.

### Key Services

#### Amazon EKS

**Purpose:** Managed Kubernetes control plane to orchestrate microservices

**Configuration:** Version 1.30+, OIDC provider enabled, public endpoint restricted by CIDR, private endpoint enabled

#### Amazon VPC

**Purpose:** Isolated network environment for the cluster resources

**Configuration:** 3 AZs, dedicated subnets for pods (CNI custom networking) and nodes

#### AWS KMS

**Purpose:** Encryption management for secrets and disk volumes

**Configuration:** Customer Managed Keys (CMK) with automatic rotation enabled

#### Amazon ECR

**Purpose:** Secure container image registry

**Configuration:** Immutable tags, image scanning on push enabled

### Network Topology

A 3-tier VPC architecture spanning 3 Availability Zones. Public subnets host NAT Gateways and Application Load Balancers. Private subnets host EKS worker nodes and internal endpoints. A separate database subnet layer is reserved for stateful persistence. Outbound traffic flows through NAT Gateways.

### Security Boundaries

Security Groups act as the primary firewall, allowing traffic only on specific ports (443 for API, specific node ports). The Control Plane is isolated in an AWS-managed VPC. Worker nodes reside in private subnets with no direct internet ingress. IAM policies define boundaries between the cluster and other AWS services.

## Alternatives Considered

### Self-Managed Kubernetes on EC2 (kops)

**Trade-offs:** Offers maximum control over the control plane and flags but requires significant operational overhead for patching, upgrading, and maintaining etcd availability.

**Rejection Reason:** High operational burden and maintenance costs outweigh the benefits of granular control.

### Amazon ECS (Elastic Container Service)

**Trade-offs:** Simpler learning curve and deep AWS integration, but lacks the rich open-source ecosystem (Helm, Operators) and portability of Kubernetes.

**Rejection Reason:** Requirement for specific Kubernetes-native tooling and potential multi-cloud portability needs.

## Implementation

### Terraform Modules

#### vpc-network

**Purpose:** Provisions VPC, Subnets, Route Tables, NAT Gateways, and NACLs

#### eks-cluster

**Purpose:** Provisions the EKS Control Plane, OIDC provider, and Cluster Security Groups

**Dependencies:** vpc-network

#### eks-node-groups

**Purpose:** Provisions Managed Node Groups and Launch Templates for worker nodes

**Dependencies:** eks-cluster

#### k8s-addons

**Purpose:** Deploys core add-ons like VPC CNI, CoreDNS, Kube-proxy, and AWS Load Balancer Controller

**Dependencies:** eks-cluster, eks-node-groups

### Provider Configuration

AWS Provider configured with default tags (Environment, Project, CostCenter) and region constraints.

### State Management

Remote state stored in S3 with versioning enabled and DynamoDB for state locking to prevent concurrent modifications.

### Deployment Order

1. Networking (VPC)
2. Security (KMS, IAM Roles)
3. EKS Control Plane
4. Worker Nodes
5. Kubernetes Add-ons

## Security

### IAM Strategy

Implementation of IAM Roles for Service Accounts (IRSA) to map Kubernetes Service Accounts to AWS IAM Roles. This ensures pods only have the specific AWS permissions they need (Least Privilege), removing the need for node-level broad permissions.

### Network Security

Strict Security Group rules referencing other Security Group IDs rather than CIDR blocks where possible. Network Policies (via Calico or VPC CNI) will be implemented to control east-west traffic between microservices within the cluster.

### Encryption

Envelope encryption enabled for Kubernetes Secrets using AWS KMS. EBS volumes for worker nodes encrypted by default using KMS. TLS 1.2+ enforced for all ingress traffic via Load Balancers.

### Compliance Controls

- AWS CloudTrail logging for all API calls
- EKS Control Plane logging enabled (Audit, API, Authenticator)
- VPC Flow Logs enabled for network traffic analysis

## Risks

### Cost overruns due to unchecked auto-scaling

**Severity:** medium

**Mitigation:** Implement Cluster Autoscaler limits, AWS Budgets alerts, and use Spot Instances for non-critical workloads.

### Kubernetes version deprecation

**Severity:** medium

**Mitigation:** Establish a quarterly upgrade cadence and use Terraform to facilitate blue/green cluster upgrades.

### Misconfigured public access to API Server

**Severity:** high

**Mitigation:** Terraform code restricts public access to specific corporate VPN CIDR blocks or disables it entirely in favor of private access.
