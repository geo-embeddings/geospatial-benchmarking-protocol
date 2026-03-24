import { Container, Heading, Text, Stack } from "@chakra-ui/react";
import { Link } from "react-router";

export default function Home() {
  return (
    <Container maxW="container.lg" py={10}>
      <Heading size="2xl">Geospatial Benchmarking Protocol</Heading>
      <Text mt={4}>Welcome to the application.</Text>
      <Stack mt={6} gap={2}>
        <Link to="/datasets">Datasets</Link>
        <Link to="/results">Results</Link>
      </Stack>
    </Container>
  );
}
