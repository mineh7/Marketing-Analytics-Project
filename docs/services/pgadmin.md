services:

  db:
    container_name: postgresql_db
    image: postgres
    restart: always
    ports:
      - 5432:5432
    environment: 
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    healthcheck:
        test: ["CMD-SHELL", "pg_isready -U postgres"]  # Healthcheck for PostgreSQL
        interval: 60s
        timeout: 10s
        retries: 5
    volumes:
      - ./postgres_data:/var/lib/postgresql/data # Persisting data
            
  pgadmin:  
    container_name: pgadmin
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_EMAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD}
      - PGADMIN_CONFIG_WTF_CSRF_ENABLED=False  # Disable CSRF for local development
    ports:
      - 5050:80 # for local browser
    volumes:
      - ./pgadmin_data:/var/lib/pgadmin  # Persisting pgAdmin configuration and sessions
    depends_on: 
      - db

  etl:
    container_name: etl
    build:
      context: ./etl
      dockerfile: Dockerfile
    ports:
      - 3000:3000
    volumes:
        - ./etl:/etl
    depends_on: 
      db:
        condition: service_healthy
    healthcheck:
      test: "exit 0"