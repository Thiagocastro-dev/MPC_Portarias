# Portarias Search and Management System

## Overview

This project aims to create a user-friendly and efficient system for searching, accessing, and managing official administrative documents ("portarias") within the Ministério Público de Contas (MPC) or similar organizations. The system leverages a three-tier architecture, incorporating a Vue.js frontend, a Python backend, and a CouchDB database. Due to the limitations of the WebContainer environment, certain advanced features, such as Natural Language Processing (NLP) techniques, are simulated.

## Table of Contents

1.  [Project Goals](#project-goals)
2.  [Technology Stack](#technology-stack)
3.  [System Architecture](#system-architecture)
4.  [Development Phases](#development-phases)
5.  [Components](#components)
6.  [Data Flow](#data-flow)
7.  [Limitations](#limitations)
8.  [Future Work](#future-work)
9.  [Setup and Deployment](#setup-and-deployment)
10. [Contributing](#contributing)
11. [License](#license)

## 1. Project Goals

*   Provide a user-friendly interface for searching and accessing "portarias" documents.
*   Automate the process of downloading, extracting, and indexing PDF documents.
*   Implement semantic search capabilities to improve the accuracy and relevance of search results.
*   Enable automated tagging and categorization of documents for better organization.
*   Create a scalable and maintainable system that can adapt to future needs.

## 2. Technology Stack

*   **Frontend:** Vue.js with Quasar Framework
*   **Backend:** Python (with standard library)
*   **Database:** CouchDB
*   **Containerization:** Docker
*   **NLP (Simulated):** Keyword-based approach

## 3. System Architecture

The system follows a three-tier architecture:

*   **Presentation Tier (Frontend):** Vue.js application for user interaction.
*   **Application Tier (Backend):** Python application for data processing and API handling.
*   **Data Tier (Database):** CouchDB database for storing document data.

## 4. Development Phases

1.  **Requirements Gathering and Analysis:**
    *   Stakeholder interviews to understand needs.
    *   Use case definition to guide development.
    *   Data analysis to understand PDF structure.
2.  **System Design:**
    *   Architecture design for component interaction.
    *   Data model design for CouchDB.
    *   UI/UX design for user-friendliness.
    *   API design for frontend-backend communication.
3.  **Implementation:**
    *   Frontend development with Vue.js and Quasar.
    *   Backend development with Python.
    *   Implementation of PDF downloading, processing, and uploading logic.
    *   Implementation of simulated semantic search and automated tagging.
    *   Integration of frontend and backend.
    *   CouchDB database setup.
4.  **Testing:**
    *   Unit tests for individual components.
    *   Integration tests for component interaction.
    *   System tests for overall functionality.
    *   User acceptance testing (UAT) with representative users.
5.  **Deployment:**
    *   Containerization with Docker.
    *   Deployment to a suitable environment (e.g., cloud platform).
    *   Application and database configuration.
6.  **Maintenance and Evolution:**
    *   Performance monitoring.
    *   Bug fixes and issue resolution.
    *   Implementation of new features and enhancements.
    *   Regular security updates.

## 5. Components

*   **Frontend:**
    *   `SearchBar.vue`: Search input and tag filtering.
    *   `PortariasList.vue`: Displays a list of portarias with summaries.
    *   `PortariaDialog.vue`: Displays the full content of a selected portaria.
    *   `TopicAnalysis.vue` (Optional): Displays the most requested topics.
    *   `LoadingSpinner.vue`: Loading indicator.
    *   `ErrorMessage.vue`: Displays error messages.
*   **Backend:**
    *   `pdf_downloader.py`: Downloads PDFs from a specified URL.
    *   `pdf_processor.py`: Extracts text content from PDFs.
    *   `db_uploader.py`: Interacts with the CouchDB database.
    *   `topic_classifier.py`: Classifies documents into topics (keyword-based).
    *   `api.py` (or similar): Defines API endpoints.
    *   `semantic_search.py` (or similar): Implements simulated semantic search.
*   **Database:**
    *   CouchDB: Stores document content, metadata, and simulated embeddings.

## 6. Data Flow

1.  `pdf_downloader.py` downloads PDFs.
2.  `pdf_processor.py` extracts text and metadata.
3.  `topic_classifier.py` classifies documents.
4.  `db_uploader.py` uploads data to CouchDB.
5.  User enters a search query in `SearchBar.vue`.
6.  Frontend sends the query to the backend.
7.  Backend queries CouchDB.
8.  Backend returns results to `PortariasList.vue`.
9.  User views full content in `PortariaDialog.vue`.

## 7. Limitations

*   **Simulated NLP:** Due to WebContainer limitations, real NLP models cannot be used.
*   **Limited Scalability:** The system may not scale well with a large number of documents or users.
*   **Data Quality:** Accuracy depends on PDF quality and OCR effectiveness.
*   **Lack of Authentication:** No user authentication or authorization is implemented.
*   **Limited Error Handling:** Basic error handling and logging are present, but more comprehensive monitoring is needed.
*   **Dependency on Specific PDF Layouts:** The document name extraction relies on hardcoded coordinates.

## 8. Future Work

*   Migrate to a more capable environment to enable real NLP.
*   Implement semantic search with actual LLM embeddings.
*   Use a dedicated vector database.
*   Improve topic classification with machine learning.
*   Implement robust authentication and authorization.
*   Enhance error handling and monitoring.
*   Develop a more flexible document name extraction method.

## 9. Setup and Deployment

1.  **Prerequisites:**
    *   Docker
    *   Docker Compose
2.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
3.  **Build and run the application:**
    ```bash
    docker-compose up --build
    ```
4.  **Access the application:**
    *   Open your web browser and navigate to the specified URL (e.g., `http://localhost:3000`).

## 10. Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.


