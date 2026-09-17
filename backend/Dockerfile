FROM eclipse-temurin:21-jdk AS build
WORKDIR /workspace
COPY . .
RUN ./mvnw -q -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
RUN useradd --system --create-home --shell /sbin/nologin appuser
COPY --from=build /workspace/target/backend-*.jar app.jar
RUN chown appuser:appuser app.jar
EXPOSE 8080
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD bash -c 'exec 3<>/dev/tcp/127.0.0.1/8080'
ENTRYPOINT ["java", "-jar", "app.jar"]