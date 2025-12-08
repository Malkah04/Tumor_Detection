"use client";

import { useState } from "react";
import axios from "axios";
import { Container, Form, Button, Alert, Spinner, Card, Image } from "react-bootstrap";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setPrediction(null);
      setError(null);

      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setPrediction(response.data.prediction);
    } catch (err) {
      console.error("Error uploading file:", err);
      setError("Failed to get prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="d-flex flex-column align-items-center justify-content-center min-vh-100">
      <Card className="p-4" style={{ width: "100%", maxWidth: "500px" }}>
        <Card.Body>
          <Card.Title as="h1" className="text-center mb-4" style={{ fontFamily: "var(--font-poppins)" }}>
            Brain Tumor Detection
          </Card.Title>
          <Form>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Upload a brain scan image</Form.Label>
              <Form.Control type="file" accept="image/*" onChange={handleFileChange} />
            </Form.Group>

            {preview && (
              <div className="text-center mb-3">
                <Image src={preview} thumbnail fluid style={{ maxHeight: "200px" }} />
              </div>
            )}

            <Button
              variant="primary"
              onClick={handleUpload}
              disabled={!selectedFile || loading}
              className="w-100"
            >
              {loading ? <Spinner animation="border" size="sm" /> : "Get Prediction"}
            </Button>
          </Form>

          {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

          {prediction && (
            <Alert variant="success" className="mt-3 text-center">
              <h4>Prediction:</h4>
              <p className="h5 text-capitalize">{prediction}</p>
            </Alert>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
}
