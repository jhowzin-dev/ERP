# Build com a plataforma do host (javac gera bytecode portável);
# apenas o stage final segue $TARGETPLATFORM (linux/amd64, linux/arm64 via buildx).
FROM --platform=$BUILDPLATFORM eclipse-temurin:21-jdk AS build
WORKDIR /workspace
COPY . .
RUN ./mvnw -q -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
RUN useradd --system --create-home --shell /sbin/nologin appuser
<<<<<<< Updated upstream
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
=======
>>>>>>> Stashed changes
COPY --from=build /workspace/target/backend-*.jar app.jar
RUN chown appuser:appuser app.jar
EXPOSE 8080
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
<<<<<<< Updated upstream
  CMD curl -f http://localhost:8080/actuator/health || exit 1
=======
  CMD bash -c 'exec 3<>/dev/tcp/127.0.0.1/8080'
>>>>>>> Stashed changes
ENTRYPOINT ["java", "-jar", "app.jar"]