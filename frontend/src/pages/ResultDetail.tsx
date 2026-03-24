import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Card,
  Code,
  Heading,
  HStack,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react";
import { Link, useParams } from "react-router";
import type { components } from "../api/types";
type Result = components["schemas"]["Result"];
import * as api from "../api/results";

export default function ResultDetail() {
  const { id } = useParams<{ id: string }>();
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api
      .getResult(id)
      .then(setResult)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <Box>
      <HStack gap={2} mb={4}>
        <Link to="/results">
          <Text color="blue.500">Results</Text>
        </Link>
        <Text color="fg.muted">/</Text>
        <Text>{id?.slice(0, 8)}...</Text>
      </HStack>
      <Heading size="2xl">Result</Heading>
      {error && (
        <Alert.Root status="error" mt={4}>
          <Alert.Title>{error}</Alert.Title>
        </Alert.Root>
      )}
      {loading && <Spinner mt={4} />}
      {result && (
        <Card.Root mt={6} variant="outline">
          <Card.Body>
            <Stack gap={4}>
              <Box>
                <Text fontWeight="medium" mb={1}>
                  ID
                </Text>
                <Code>{id}</Code>
              </Box>
              <Box>
                <Text fontWeight="medium" mb={1}>
                  Dataset
                </Text>
                <Link to={`/datasets/${result.dataset_id}`}>
                  <Code color="blue.500">{result.dataset_id}</Code>
                </Link>
              </Box>
            </Stack>
          </Card.Body>
        </Card.Root>
      )}
    </Box>
  );
}
