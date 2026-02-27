# ── Build stage ────────────────────────────────────────────
FROM maven:3.9-eclipse-temurin-17 AS build

WORKDIR /build
COPY pom.xml .
# Download dependencies first (cached layer)
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn package -DskipTests -B

# ── Runtime stage ─────────────────────────────────────────
FROM eclipse-temurin:17-jre-alpine

LABEL maintainer="Supervertaler"
LABEL description="Okapi Framework sidecar for document extraction and merge"

WORKDIR /app
COPY --from=build /build/target/okapi-sidecar-*.jar okapi-sidecar.jar

# Non-root user for security
RUN addgroup -S sidecar && adduser -S sidecar -G sidecar
USER sidecar

EXPOSE 8090

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD wget -qO- http://127.0.0.1:8090/health || exit 1

ENTRYPOINT ["java", "-jar", "okapi-sidecar.jar"]
CMD ["--port=8090"]
