import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Card,
  Code,
  Heading,
  HStack,
  Spinner,
  Text,
} from "@chakra-ui/react";
import { Link, useParams } from "react-router";
import type { components } from "../api/types";
type Dataset = components["schemas"]["Dataset"];
import * as api from "../api/datasets";

export default function DatasetDetail() {
  const { id } = useParams<{ id: string }>();
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api
      .getDataset(id)
      .then(setDataset)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <Box>
      <HStack gap={2} mb={4}>
        <Link to="/datasets">
          <Text color="brand.500">Datasets</Text>
        </Link>
        <Text color="fg.muted">/</Text>
        <Text>{id?.slice(0, 8)}...</Text>
      </HStack>
      <Heading size="2xl">Dataset</Heading>
      {error && (
        <Alert.Root status="error" mt={4}>
          <Alert.Title>{error}</Alert.Title>
        </Alert.Root>
      )}
      {loading && <Spinner mt={4} />}
      {dataset && (
        <Card.Root mt={6} variant="outline">
          <Card.Body>
            <Text fontWeight="medium" mb={1}>
              ID
            </Text>
            <Code>{id}</Code>
          </Card.Body>
        </Card.Root>
      )}
    </Box>
  );
}
