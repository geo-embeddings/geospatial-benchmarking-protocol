import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Badge,
  Box,
  Button,
  Dialog,
  Fieldset,
  Flex,
  Heading,
  HStack,
  Input,
  Portal,
  Stack,
  Table,
  Text,
} from "@chakra-ui/react";
import { Link } from "react-router";
import type { components } from "../api/types";
type Dataset = components["schemas"]["Dataset"];
import * as api from "../api/datasets";

const INITIAL_FORM = {
  title: "",
  tags: "",
};

export default function Datasets() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [version, setVersion] = useState(0);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState(INITIAL_FORM);

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

  function updateField(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleCreate() {
    try {
      setError(null);
      const tags = form.tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);

      await api.createDataset({ title: form.title, tags } as Omit<
        Dataset,
        "id"
      >);
      setForm(INITIAL_FORM);
      setOpen(false);
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

  const canSubmit = form.title.trim() !== "";

  return (
    <Box>
      <Flex justify="space-between" align="center">
        <Heading size="2xl">Datasets</Heading>
        <Dialog.Root
          open={open}
          onOpenChange={(e) => setOpen(e.open)}
          size="lg"
        >
          <Dialog.Trigger asChild>
            <Button colorPalette="brand">Create Dataset</Button>
          </Dialog.Trigger>
          <Portal>
            <Dialog.Backdrop />
            <Dialog.Positioner>
              <Dialog.Content>
                <Dialog.Header>
                  <Dialog.Title>Create Dataset</Dialog.Title>
                  <Dialog.Description>
                    Create a new STAC Item dataset
                  </Dialog.Description>
                </Dialog.Header>
                <Dialog.Body>
                  <Stack gap={4}>
                    <Fieldset.Root>
                      <Fieldset.Legend>Required</Fieldset.Legend>
                      <Box>
                        <Text fontWeight="medium" mb={1}>
                          Title
                        </Text>
                        <Input
                          placeholder="Dataset title"
                          value={form.title}
                          onChange={(e) => updateField("title", e.target.value)}
                        />
                      </Box>
                    </Fieldset.Root>

                    <Fieldset.Root>
                      <Fieldset.Legend>Metadata</Fieldset.Legend>
                      <Box>
                        <Text fontWeight="medium" mb={1}>
                          Tags
                        </Text>
                        <Input
                          placeholder="Comma-separated tags"
                          value={form.tags}
                          onChange={(e) => updateField("tags", e.target.value)}
                        />
                      </Box>
                    </Fieldset.Root>
                  </Stack>
                </Dialog.Body>
                <Dialog.Footer>
                  <Dialog.ActionTrigger asChild>
                    <Button variant="outline">Cancel</Button>
                  </Dialog.ActionTrigger>
                  <Button
                    colorPalette="brand"
                    onClick={handleCreate}
                    disabled={!canSubmit}
                  >
                    Create
                  </Button>
                </Dialog.Footer>
                <Dialog.CloseTrigger />
              </Dialog.Content>
            </Dialog.Positioner>
          </Portal>
        </Dialog.Root>
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
              <Table.ColumnHeader>Title</Table.ColumnHeader>
              <Table.ColumnHeader>Tags</Table.ColumnHeader>
              <Table.ColumnHeader textAlign="end">Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {datasets.map((dataset) => (
              <Table.Row key={dataset.id}>
                <Table.Cell>
                  <Link to={`/datasets/${dataset.id}`}>{dataset.title}</Link>
                </Table.Cell>
                <Table.Cell>
                  <HStack gap={1} flexWrap="wrap">
                    {(dataset.tags ?? []).map((tag) => (
                      <Badge key={tag} colorPalette="brand" variant="subtle">
                        {tag}
                      </Badge>
                    ))}
                  </HStack>
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
