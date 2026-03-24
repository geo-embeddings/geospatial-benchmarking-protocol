import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Code,
  Flex,
  Heading,
  HStack,
  Table,
  Text,
} from "@chakra-ui/react";
import { Link } from "react-router";
import type { components } from "../api/types";
type Dataset = components["schemas"]["Dataset"];
import * as api from "../api/datasets";

export default function Datasets() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
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
      setError(null);
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

  return (
    <Box>
      <Flex justify="space-between" align="center">
        <Heading size="2xl">Datasets</Heading>
        <Button colorPalette="blue" onClick={handleCreate}>
          Create Dataset
        </Button>
      </Flex>
      {error && (
        <Alert.Root status="error" mt={4}>
          <Alert.Title>{error}</Alert.Title>
        </Alert.Root>
      )}
      {datasets.length === 0 ? (
        <Text mt={6} color="fg.muted">
          No datasets yet. Create one to get started.
        </Text>
      ) : (
        <Table.Root mt={6} variant="outline">
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader textAlign="end">Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {datasets.map((dataset) => (
              <Table.Row key={dataset.id}>
                <Table.Cell>
                  <Link to={`/datasets/${dataset.id}`}>
                    <Code>{dataset.id}</Code>
                  </Link>
                </Table.Cell>
                <Table.Cell textAlign="end">
                  <HStack justify="end" gap={2}>
                    <Link to={`/datasets/${dataset.id}`}>
                      <Button size="xs" variant="outline">
                        View
                      </Button>
                    </Link>
                    <Button
                      size="xs"
                      colorPalette="red"
                      variant="outline"
                      onClick={() => handleDelete(dataset.id!)}
                    >
                      Delete
                    </Button>
                  </HStack>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      )}
    </Box>
  );
}
