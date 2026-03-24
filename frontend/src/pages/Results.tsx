import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Badge,
  Box,
  Button,
  Code,
  Flex,
  Heading,
  HStack,
  Input,
  Table,
  Text,
} from "@chakra-ui/react";
import { Link } from "react-router";
import type { components } from "../api/types";
type Result = components["schemas"]["Result"];
type Dataset = components["schemas"]["Dataset"];
import * as api from "../api/results";
import * as datasetsApi from "../api/datasets";

export default function Results() {
  const [results, setResults] = useState<Result[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [datasetId, setDatasetId] = useState("");
  const [filterTag, setFilterTag] = useState("");
  const [version, setVersion] = useState(0);

  const reload = useCallback(() => setVersion((v) => v + 1), []);

  const allTags = [...new Set(datasets.flatMap((d) => d.tags ?? []))].sort();

  useEffect(() => {
    let cancelled = false;
    datasetsApi
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

  useEffect(() => {
    let cancelled = false;
    api
      .listResults(filterTag || undefined)
      .then((data) => {
        if (!cancelled) setResults(data);
      })
      .catch((e) => {
        if (!cancelled) setError(String(e));
      });
    return () => {
      cancelled = true;
    };
  }, [version, filterTag]);

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

  return (
    <Box>
      <Flex justify="space-between" align="center">
        <Heading size="2xl">Results</Heading>
        <HStack>
          {allTags.map((tag) => (
            <Badge
              key={tag}
              colorPalette={filterTag === tag ? "brand" : "gray"}
              variant={filterTag === tag ? "solid" : "subtle"}
              cursor="pointer"
              onClick={() => setFilterTag(filterTag === tag ? "" : tag)}
            >
              {tag}
            </Badge>
          ))}
          {filterTag && (
            <Button size="xs" variant="ghost" onClick={() => setFilterTag("")}>
              Clear
            </Button>
          )}
        </HStack>
      </Flex>
      {error && (
        <Alert.Root status="error" mt={4}>
          <Alert.Title>{error}</Alert.Title>
        </Alert.Root>
      )}
      <Flex mt={6} gap={2}>
        <Input
          placeholder="Dataset ID"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
          flex={1}
        />
        <Button colorPalette="brand" onClick={handleCreate}>
          Create Result
        </Button>
      </Flex>
      {results.length === 0 ? (
        <Text mt={6} color="fg.muted">
          No results yet. Create one to get started.
        </Text>
      ) : (
        <Table.Root mt={6} variant="outline">
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader>Dataset</Table.ColumnHeader>
              <Table.ColumnHeader textAlign="end">Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {results.map((result) => (
              <Table.Row key={result.id}>
                <Table.Cell>
                  <Link to={`/results/${result.id}`}>
                    <Code>{result.id}</Code>
                  </Link>
                </Table.Cell>
                <Table.Cell>
                  <Link to={`/datasets/${result.dataset_id}`}>
                    <Code color="brand.500">{result.dataset_id}</Code>
                  </Link>
                </Table.Cell>
                <Table.Cell textAlign="end">
                  <HStack justify="end" gap={2}>
                    <Link to={`/results/${result.id}`}>
                      <Button size="xs" variant="outline">
                        View
                      </Button>
                    </Link>
                    <Button
                      size="xs"
                      colorPalette="red"
                      variant="outline"
                      onClick={() => handleDelete(result.id!)}
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
