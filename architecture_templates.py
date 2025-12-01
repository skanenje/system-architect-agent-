"""
Architecture Templates

Defines common architecture patterns with their typical components,
data flows, and characteristics.
"""

from typing import Dict, List, Any


class ArchitectureTemplates:
    """
    Collection of architecture pattern templates.
    Each template defines typical components and data flows.
    """
    
    @staticmethod
    def get_monolith_template() -> Dict[str, Any]:
        """
        Monolith architecture template.
        Best for: Small to medium apps, MVPs, simple requirements.
        """
        return {
            "style": "monolith",
            "description": "Single unified application with all components in one codebase",
            "characteristics": [
                "Simple deployment",
                "Easy local development",
                "Shared database",
                "Tight coupling between components",
                "Scales vertically"
            ],
            "typical_components": [
                {
                    "name": "Web Application Server",
                    "type": "application",
                    "purpose": "Handles HTTP requests, business logic, and rendering",
                    "technologies": ["Node.js + Express", "Django", "Ruby on Rails", "Spring Boot"]
                },
                {
                    "name": "Database",
                    "type": "data_store",
                    "purpose": "Persistent data storage",
                    "technologies": ["PostgreSQL", "MySQL", "MongoDB"]
                },
                {
                    "name": "Cache Layer",
                    "type": "cache",
                    "purpose": "Speed up frequent queries and reduce database load",
                    "technologies": ["Redis", "Memcached"],
                    "optional": True
                },
                {
                    "name": "Background Job Processor",
                    "type": "worker",
                    "purpose": "Handle async tasks (emails, reports, etc.)",
                    "technologies": ["Celery", "Sidekiq", "Bull"],
                    "optional": True
                }
            ],
            "typical_data_flows": [
                {
                    "from": "Client",
                    "to": "Web Application Server",
                    "data": "HTTP requests",
                    "protocol": "HTTP/HTTPS"
                },
                {
                    "from": "Web Application Server",
                    "to": "Database",
                    "data": "SQL queries",
                    "protocol": "Database protocol"
                },
                {
                    "from": "Web Application Server",
                    "to": "Cache Layer",
                    "data": "Cache read/write",
                    "protocol": "Redis protocol"
                }
            ]
        }
    
    @staticmethod
    def get_microservices_template() -> Dict[str, Any]:
        """
        Microservices architecture template.
        Best for: Large scale, multiple teams, complex domains.
        """
        return {
            "style": "microservices",
            "description": "Distributed system with independent, loosely-coupled services",
            "characteristics": [
                "Independent deployment",
                "Technology diversity",
                "Fault isolation",
                "Complex operations",
                "Scales horizontally"
            ],
            "typical_components": [
                {
                    "name": "API Gateway",
                    "type": "gateway",
                    "purpose": "Single entry point, routing, authentication, rate limiting",
                    "technologies": ["Kong", "AWS API Gateway", "Nginx", "Traefik"]
                },
                {
                    "name": "Service A (Domain Service)",
                    "type": "microservice",
                    "purpose": "Handles specific business domain logic",
                    "technologies": ["Any language/framework"]
                },
                {
                    "name": "Service B (Domain Service)",
                    "type": "microservice",
                    "purpose": "Handles another business domain",
                    "technologies": ["Any language/framework"]
                },
                {
                    "name": "Service Database (per service)",
                    "type": "data_store",
                    "purpose": "Each service owns its data",
                    "technologies": ["PostgreSQL", "MongoDB", "DynamoDB"]
                },
                {
                    "name": "Message Queue",
                    "type": "messaging",
                    "purpose": "Async communication between services",
                    "technologies": ["RabbitMQ", "Kafka", "AWS SQS"]
                },
                {
                    "name": "Service Discovery",
                    "type": "infrastructure",
                    "purpose": "Services find each other dynamically",
                    "technologies": ["Consul", "Eureka", "Kubernetes DNS"]
                },
                {
                    "name": "Distributed Tracing",
                    "type": "observability",
                    "purpose": "Track requests across services",
                    "technologies": ["Jaeger", "Zipkin", "AWS X-Ray"]
                }
            ],
            "typical_data_flows": [
                {
                    "from": "Client",
                    "to": "API Gateway",
                    "data": "HTTP requests",
                    "protocol": "HTTP/HTTPS"
                },
                {
                    "from": "API Gateway",
                    "to": "Microservices",
                    "data": "Routed requests",
                    "protocol": "HTTP/gRPC"
                },
                {
                    "from": "Service A",
                    "to": "Service B",
                    "data": "Service-to-service calls",
                    "protocol": "HTTP/gRPC/Message Queue"
                },
                {
                    "from": "Microservice",
                    "to": "Own Database",
                    "data": "Data operations",
                    "protocol": "Database protocol"
                }
            ]
        }
    
    @staticmethod
    def get_event_driven_template() -> Dict[str, Any]:
        """
        Event-driven architecture template.
        Best for: Real-time systems, high throughput, decoupled systems.
        """
        return {
            "style": "event-driven",
            "description": "System driven by events and asynchronous message passing",
            "characteristics": [
                "Loose coupling",
                "High scalability",
                "Eventual consistency",
                "Complex debugging",
                "Real-time capabilities"
            ],
            "typical_components": [
                {
                    "name": "Event Producer",
                    "type": "producer",
                    "purpose": "Generates events when state changes occur",
                    "technologies": ["Application services", "IoT devices", "User actions"]
                },
                {
                    "name": "Event Bus / Message Broker",
                    "type": "messaging",
                    "purpose": "Routes events to interested consumers",
                    "technologies": ["Apache Kafka", "AWS EventBridge", "RabbitMQ", "Azure Event Hubs"]
                },
                {
                    "name": "Event Consumer / Handler",
                    "type": "consumer",
                    "purpose": "Subscribes to events and processes them",
                    "technologies": ["Lambda functions", "Worker services", "Stream processors"]
                },
                {
                    "name": "Event Store",
                    "type": "data_store",
                    "purpose": "Persistent log of all events (event sourcing)",
                    "technologies": ["Kafka", "EventStoreDB", "DynamoDB Streams"],
                    "optional": True
                },
                {
                    "name": "Read Model / Materialized View",
                    "type": "data_store",
                    "purpose": "Optimized views for queries (CQRS pattern)",
                    "technologies": ["PostgreSQL", "Elasticsearch", "Redis"]
                },
                {
                    "name": "Stream Processor",
                    "type": "processor",
                    "purpose": "Real-time event processing and aggregation",
                    "technologies": ["Kafka Streams", "Apache Flink", "AWS Kinesis"],
                    "optional": True
                }
            ],
            "typical_data_flows": [
                {
                    "from": "Event Producer",
                    "to": "Event Bus",
                    "data": "Events (state changes)",
                    "protocol": "Kafka protocol / AMQP / HTTP"
                },
                {
                    "from": "Event Bus",
                    "to": "Event Consumers",
                    "data": "Event notifications",
                    "protocol": "Push/Pull subscription"
                },
                {
                    "from": "Event Consumer",
                    "to": "Read Model",
                    "data": "Update materialized views",
                    "protocol": "Database writes"
                }
            ]
        }
    
    @staticmethod
    def get_agentic_template() -> Dict[str, Any]:
        """
        Agentic workflow architecture template.
        Best for: AI-powered applications, autonomous systems, complex decision-making.
        """
        return {
            "style": "agentic",
            "description": "AI agents orchestrate workflows and make autonomous decisions",
            "characteristics": [
                "Autonomous decision-making",
                "Tool/API integration",
                "Conversational interfaces",
                "State management",
                "Human-in-the-loop capabilities"
            ],
            "typical_components": [
                {
                    "name": "Agent Orchestrator",
                    "type": "orchestrator",
                    "purpose": "Coordinates multiple agents and workflows",
                    "technologies": ["LangChain", "AutoGPT", "Custom orchestration"]
                },
                {
                    "name": "LLM Service",
                    "type": "ai_service",
                    "purpose": "Provides language understanding and generation",
                    "technologies": ["OpenAI API", "Anthropic Claude", "Google Gemini", "Local LLMs"]
                },
                {
                    "name": "Agent Memory / State Store",
                    "type": "data_store",
                    "purpose": "Maintains conversation history and agent state",
                    "technologies": ["Vector DB (Pinecone, Weaviate)", "Redis", "PostgreSQL"]
                },
                {
                    "name": "Tool Registry",
                    "type": "registry",
                    "purpose": "Available tools/APIs agents can use",
                    "technologies": ["Function calling", "API integrations", "Custom tools"]
                },
                {
                    "name": "Vector Database",
                    "type": "data_store",
                    "purpose": "Semantic search and RAG (Retrieval Augmented Generation)",
                    "technologies": ["Pinecone", "Weaviate", "ChromaDB", "Qdrant"]
                },
                {
                    "name": "Task Queue",
                    "type": "queue",
                    "purpose": "Manages async agent tasks",
                    "technologies": ["Celery", "BullMQ", "AWS SQS"]
                },
                {
                    "name": "User Interface",
                    "type": "interface",
                    "purpose": "Chat interface or API for user interaction",
                    "technologies": ["Web chat UI", "REST API", "WebSocket"]
                }
            ],
            "typical_data_flows": [
                {
                    "from": "User",
                    "to": "Agent Orchestrator",
                    "data": "User request/query",
                    "protocol": "HTTP/WebSocket"
                },
                {
                    "from": "Agent Orchestrator",
                    "to": "LLM Service",
                    "data": "Prompts and context",
                    "protocol": "HTTP API"
                },
                {
                    "from": "Agent Orchestrator",
                    "to": "Vector Database",
                    "data": "Semantic search queries",
                    "protocol": "Vector DB API"
                },
                {
                    "from": "Agent Orchestrator",
                    "to": "Tool Registry",
                    "data": "Tool invocations",
                    "protocol": "Function calls / HTTP"
                },
                {
                    "from": "Agent Orchestrator",
                    "to": "Agent Memory",
                    "data": "State updates",
                    "protocol": "Database writes"
                }
            ]
        }
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available architecture templates."""
        return {
            "monolith": ArchitectureTemplates.get_monolith_template(),
            "microservices": ArchitectureTemplates.get_microservices_template(),
            "event-driven": ArchitectureTemplates.get_event_driven_template(),
            "agentic": ArchitectureTemplates.get_agentic_template()
        }
    
    @staticmethod
    def get_template(style: str) -> Dict[str, Any]:
        """
        Get a specific template by style name.
        
        Args:
            style: One of 'monolith', 'microservices', 'event-driven', 'agentic'
            
        Returns:
            Template dictionary
            
        Raises:
            ValueError if style is invalid
        """
        templates = ArchitectureTemplates.get_all_templates()
        if style not in templates:
            raise ValueError(f"Invalid architecture style: {style}. Must be one of: {list(templates.keys())}")
        return templates[style]
