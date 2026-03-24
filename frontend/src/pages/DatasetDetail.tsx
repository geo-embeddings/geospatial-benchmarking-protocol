import { useEffect, useState } from "react";
import { Container, Heading, Text } from "@chakra-ui/react";
import { Link, useParams } from "react-router";
import type { components } from "../api/types";
type Dataset = components["schemas"]["Dataset"];
import * as api from "../api/datasets";

export default function DatasetDetail() {
  const { id } = useParams<{ id: string }>();
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    api
      .getDataset(id)
      .then(setDataset)
      .catch((e) => setError(String(e)));
  }, [id]);

  return (
    <Container maxW="container.lg" py={10}>
      <Link to="/datasets">← Datasets</Link>
      <Heading size="2xl" mt={4}>
        Dataset
      </Heading>
      {error && (
        <Text color="red.500" mt={2}>
          {error}
        </Text>
      )}
      {dataset && (
        <Text mt={4}>
          <code>{id}</code>
        </Text>
      )}
    </Container>
  );
}
