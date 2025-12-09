"use client";

import { useState } from "react";
import axios from "axios";
import { Container, Form, Button, Alert, Spinner, Card, Image, ProgressBar } from "react-bootstrap";

interface PredictionResult {
  prediction: string;
  confidence: number;
  probabilities: Record<string, number>;
  filename: string;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setResult(null);
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
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await axios.post(`${apiUrl}/predict`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data);
    } catch (err) {
      console.error("Error uploading file:", err);
      if (axios.isAxiosError(err) && err.response) {
        setError(`Error: ${err.response.data.detail || "Failed to get prediction"}`);
      } else {
        setError("Failed to connect to the API. Please ensure the backend is running.");
      }
    } finally {
      setLoading(false);
    }
  };

  const getTumorDisplayName = (tumorType: string): string => {
    const displayNames: Record<string, string> = {
      glioma: "Glioma",
      meningioma: "Meningioma",
      notumor: "No Tumor",
      pituitary: "Pituitary Tumor",
    };
    return displayNames[tumorType] || tumorType;
  };

  const getTumorColor = (tumorType: string): string => {
    const colors: Record<string, string> = {
      glioma: "#dc3545",
      meningioma: "#fd7e14",
      notumor: "#28a745",
      pituitary: "#6610f2",
    };
    return colors[tumorType] || "#007bff";
  };

  return (
    <Container className="d-flex flex-column align-items-center justify-content-center min-vh-100 py-5">
      <Card className="p-4" style={{ width: "100%", maxWidth: "600px" }}>
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

          {result && (
            <div className="mt-4">
              <Card className="mb-3 border-0 shadow-sm">
                <Card.Body>
                  <h5 className="mb-3">
                    <strong>Prediction Results</strong>
                  </h5>
                  <div className="mb-3">
                    <p className="mb-1">
                      <strong>Detected:</strong>{" "}
                      <span
                        className="h5"
                        style={{ color: getTumorColor(result.prediction) }}
                      >
                        {getTumorDisplayName(result.prediction)}
                      </span>
                    </p>
                    <p className="mb-1">
                      <strong>Confidence:</strong>{" "}
                      <span className="text-primary">
                        {(result.confidence * 100).toFixed(2)}%
                      </span>
                    </p>
                    <p className="mb-0 text-muted" style={{ fontSize: "0.9rem" }}>
                      <strong>File:</strong> {result.filename}
                    </p>
                  </div>

                  <div className="mt-3">
                    <h6 className="mb-3">Probability Distribution:</h6>
                    {Object.entries(result.probabilities)
                      .sort((a, b) => b[1] - a[1])
                      .map(([tumorType, probability]) => (
                        <div key={tumorType} className="mb-3">
                          <div className="d-flex justify-content-between mb-1">
                            <span className="text-capitalize">
                              {getTumorDisplayName(tumorType)}
                            </span>
                            <span className="text-muted">
                              {(probability * 100).toFixed(2)}%
                            </span>
                          </div>
                          <ProgressBar
                            now={probability * 100}
                            variant={
                              tumorType === result.prediction
                                ? "success"
                                : "secondary"
                            }
                            style={{
                              height: "8px",
                              backgroundColor:
                                tumorType === result.prediction
                                  ? undefined
                                  : "#e9ecef",
                            }}
                          />
                        </div>
                      ))}
                  </div>
                </Card.Body>
              </Card>
            </div>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
}
