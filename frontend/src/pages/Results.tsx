import { useCallback, useEffect, useState } from "react";
import {
  Button,
  Container,
  Heading,
  Input,
  Stack,
  Table,
  Text,
} from "@chakra-ui/react";
import { Link } from "react-router";
import type { components } from "../api/types";
type Result = components["schemas"]["Result"];
import * as api from "../api/results";

export default function Results() {
  const [results, setResults] = useState<Record<string, Result>>({});
  const [error, setError] = useState<string | null>(null);
  const [datasetId, setDatasetId] = useState("");
  const [version, setVersion] = useState(0);

  const reload = useCallback(() => setVersion((v) => v + 1), []);

  useEffect(() => {
    let cancelled = false;
    api
      .listResults()
      .then((data) => {
        if (!cancelled) setResults(data);
      })
      .catch((e) => {
        if (!cancelled) setError(String(e));
      });
    return () => {
      cancelled = true;
    };
  }, [version]);

  async function handleCreate() {
    if (!datasetId.trim()) {
      setError("Dataset ID is required");
      return;
    }
    try {
      setError(null);
      await api.createResult({ dataset_id: datasetId.trim() });
      setDatasetId("");
      reload();
    } catch (e) {
      setError(String(e));
    }
  }

  async function handleDelete(id: string) {
    try {
      await api.deleteResult(id);
      reload();
    } catch (e) {
      setError(String(e));
    }
  }

  const entries = Object.entries(results);

  return (
    <Container maxW="container.lg" py={10}>
      <Link to="/">← Home</Link>
      <Heading size="2xl" mt={4}>
        Results
      </Heading>
      {error && (
        <Text color="red.500" mt={2}>
          {error}
        </Text>
      )}
      <Stack direction="row" mt={4} gap={2}>
        <Input
          placeholder="Dataset ID"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
        />
        <Button onClick={handleCreate}>Create Result</Button>
      </Stack>
      {entries.length === 0 ? (
        <Text mt={4}>No results yet.</Text>
      ) : (
        <Table.Root mt={4}>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader>Dataset ID</Table.ColumnHeader>
              <Table.ColumnHeader>Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {entries.map(([id, result]) => (
              <Table.Row key={id}>
                <Table.Cell>
                  <code>{id}</code>
                </Table.Cell>
                <Table.Cell>
                  <Link to={`/datasets/${result.dataset_id}`}>
                    <code>{result.dataset_id}</code>
                  </Link>
                </Table.Cell>
                <Table.Cell>
                  <Stack direction="row" gap={2}>
                    <Link to={`/results/${id}`}>View</Link>
                    <Button size="xs" onClick={() => handleDelete(id)}>
                      Delete
                    </Button>
                  </Stack>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      )}
    </Container>
  );
}
