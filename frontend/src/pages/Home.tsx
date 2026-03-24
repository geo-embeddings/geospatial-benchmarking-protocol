import { Box, Card, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import { Link } from "react-router";

export default function Home() {
  return (
    <Box>
      <Heading size="2xl">Geospatial Benchmarking Protocol</Heading>
      <Text mt={4} color="fg.muted">
        Manage datasets and benchmark results.
      </Text>
      <SimpleGrid columns={{ base: 1, md: 2 }} gap={6} mt={8}>
        <Link to="/datasets">
          <Card.Root variant="outline" _hover={{ shadow: "md" }}>
            <Card.Header>
              <Heading size="md">Datasets</Heading>
            </Card.Header>
            <Card.Body>
              <Text color="fg.muted">View and manage benchmark datasets.</Text>
            </Card.Body>
          </Card.Root>
        </Link>
        <Link to="/results">
          <Card.Root variant="outline" _hover={{ shadow: "md" }}>
            <Card.Header>
              <Heading size="md">Results</Heading>
            </Card.Header>
            <Card.Body>
              <Text color="fg.muted">View and manage benchmark results.</Text>
            </Card.Body>
          </Card.Root>
        </Link>
      </SimpleGrid>
    </Box>
  );
}
