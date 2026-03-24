import { useCallback, useEffect, useState } from "react";
import {
  Button,
  Container,
  Heading,
  Stack,
  Table,
  Text,
} from "@chakra-ui/react";
import { Link } from "react-router";
import type { components } from "../api/types";
type Dataset = components["schemas"]["Dataset"];
import * as api from "../api/datasets";

export default function Datasets() {
  const [datasets, setDatasets] = useState<Record<string, Dataset>>({});
  const [error, setError] = useState<string | null>(null);
  const [version, setVersion] = useState(0);

  const reload = useCallback(() => setVersion((v) => v + 1), []);

  useEffect(() => {
    let cancelled = false;
    api
      .listDatasets()
      .then((data) => {
        if (!cancelled) setDatasets(data);
      })
      .catch((e) => {
        if (!cancelled) setError(String(e));
      });
    return () => {
      cancelled = true;
    };
  }, [version]);

  async function handleCreate() {
    try {
      await api.createDataset({});
      reload();
    } catch (e) {
      setError(String(e));
    }
  }

  async function handleDelete(id: string) {
    try {
      await api.deleteDataset(id);
      reload();
    } catch (e) {
      setError(String(e));
    }
  }

  const entries = Object.entries(datasets);

  return (
    <Container maxW="container.lg" py={10}>
      <Link to="/">← Home</Link>
      <Heading size="2xl" mt={4}>
        Datasets
      </Heading>
      {error && (
        <Text color="red.500" mt={2}>
          {error}
        </Text>
      )}
      <Button mt={4} onClick={handleCreate}>
        Create Dataset
      </Button>
      {entries.length === 0 ? (
        <Text mt={4}>No datasets yet.</Text>
      ) : (
        <Table.Root mt={4}>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader>Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {entries.map(([id]) => (
              <Table.Row key={id}>
                <Table.Cell>
                  <code>{id}</code>
                </Table.Cell>
                <Table.Cell>
                  <Stack direction="row" gap={2}>
                    <Link to={`/datasets/${id}`}>View</Link>
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
