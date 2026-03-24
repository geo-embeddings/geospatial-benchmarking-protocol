import { useEffect, useState } from "react";
import { Container, Heading, Stack, Text } from "@chakra-ui/react";
import { Link, useParams } from "react-router";
import type { components } from "../api/types";
type Result = components["schemas"]["Result"];
import * as api from "../api/results";

export default function ResultDetail() {
  const { id } = useParams<{ id: string }>();
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    api
      .getResult(id)
      .then(setResult)
      .catch((e) => setError(String(e)));
  }, [id]);

  return (
    <Container maxW="container.lg" py={10}>
      <Link to="/results">← Results</Link>
      <Heading size="2xl" mt={4}>
        Result
      </Heading>
      {error && (
        <Text color="red.500" mt={2}>
          {error}
        </Text>
      )}
      {result && (
        <Stack mt={4} gap={2}>
          <Text>
            ID: <code>{id}</code>
          </Text>
          <Text>
            Dataset:{" "}
            <Link to={`/datasets/${result.dataset_id}`}>
              <code>{result.dataset_id}</code>
            </Link>
          </Text>
        </Stack>
      )}
    </Container>
  );
}
