FROM alpine:latest
WORKDIR /data
# Copy your products file into the image
COPY products.json .
# Command to copy it to the shared pod volume when it boots
CMD ["cp", "products.json", "/shared/products.json"]
