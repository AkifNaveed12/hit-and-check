# Hit & Check Architecture

This file contains Mermaid diagrams for system architecture, user flow, data flow, and low-level module design.

## High-Level System Architecture

```mermaid
flowchart LR
    User[User] --> UI[Streamlit UI]
    UI --> Validation[Input Validation]
    UI --> Transform[PIN Transformation]
    Transform --> Attack[Attack Simulator]
    Attack --> Scoring[Scoring Engine]
    Scoring --> Dashboard[Dashboard and Charts]
    Scoring --> ReportBuilder[Report Payload Builder]
    ReportBuilder --> Groq[Groq API]
    Groq --> AIReport[AI Report Renderer]
    Dashboard --> EmailBuilder[Email Report Builder]
    AIReport --> EmailBuilder
    EmailBuilder --> SMTP[SMTP Provider]
    SMTP --> Inbox[User Inbox]
    UI --> Awareness[Safe Awareness Demo]
```

## User Flow

```mermaid
flowchart TD
    Start([Open App]) --> Notice[Read Safety Notice]
    Notice --> Form[Enter Name, Email, Demo PIN]
    Form --> SelectAlgo[Select Transformation]
    SelectAlgo --> SelectAttack[Select Attack Type]
    SelectAttack --> Run[Run Analysis]
    Run --> Valid{Input Valid?}
    Valid -- No --> Error[Show Validation Error]
    Error --> Form
    Valid -- Yes --> Encrypt[Transform Demo PIN]
    Encrypt --> Simulate[Run Attack Simulation]
    Simulate --> Score[Calculate Scores]
    Score --> Dash[Display Dashboard]
    Dash --> AI{Generate AI Report?}
    AI -- Yes --> Groq[Send JSON to Groq]
    AI -- No --> Continue[Continue Reviewing]
    Groq --> Report[Display Report]
    Dash --> Mail{Email Report?}
    Mail -- Yes --> Send[Send Report Email]
    Mail -- No --> Continue
    Dash --> Demo{Run Awareness Demo?}
    Demo -- Yes --> Awareness[In-App Safe Demo]
    Demo -- No --> Continue
```

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit App
    participant V as Validators
    participant E as Encryption Module
    participant A as Attack Module
    participant C as Scoring Module
    participant R as Report Builder
    participant G as Groq API
    participant M as Email Service

    U->>S: Submit demo PIN and options
    S->>V: Validate PIN and email
    V-->>S: Validation result
    S->>E: Transform demo PIN
    E-->>S: Transformed PIN
    S->>A: Simulate selected attack
    A-->>S: Attack result
    S->>C: Calculate risk metrics
    C-->>S: Score result
    S->>R: Build strict JSON payload
    R-->>S: Report payload
    S->>G: Request AI report
    G-->>S: JSON report
    S->>M: Send email report if requested
    M-->>U: Email delivered
```

## Low-Level Module Architecture

```mermaid
flowchart TB
    app[app.py]

    subgraph src[src package]
        config[config.py]
        validators[validators.py]
        encryption[encryption.py]
        attacks[attacks.py]
        scoring[scoring.py]
        report_builder[report_builder.py]
        groq_client[groq_client.py]
        email_service[email_service.py]
        awareness_demo[awareness_demo.py]
    end

    subgraph data[data]
        commonPins[common_pins.json]
    end

    subgraph prompts[prompts]
        reportPrompt[pin_report_prompt.txt]
        chatPrompt[chatbot_prompt.txt]
    end

    app --> config
    app --> validators
    app --> encryption
    app --> attacks
    app --> scoring
    app --> report_builder
    app --> groq_client
    app --> email_service
    app --> awareness_demo
    attacks --> commonPins
    report_builder --> reportPrompt
    groq_client --> chatPrompt
```

## Deployment Architecture

```mermaid
flowchart LR
    Dev[Local Development] --> GitHub[GitHub Repository]
    GitHub --> Streamlit[Streamlit Community Cloud]
    Streamlit --> Secrets[Streamlit Secrets]
    Secrets --> App[Running App]
    App --> Groq[Groq API]
    App --> SMTP[SMTP Provider]
```

