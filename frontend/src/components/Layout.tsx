import { Box, Container, Flex, Heading, HStack } from "@chakra-ui/react";
import { Link, Outlet } from "react-router";

export default function Layout() {
  return (
    <Box minH="100vh">
      <Box as="nav" bg="blue.600" color="white" py={3} px={4}>
        <Container maxW="container.lg">
          <Flex justify="space-between" align="center">
            <Link to="/">
              <Heading size="md" fontWeight="bold">
                GBP
              </Heading>
            </Link>
            <HStack gap={6}>
              <Link to="/datasets">Datasets</Link>
              <Link to="/results">Results</Link>
            </HStack>
          </Flex>
        </Container>
      </Box>
      <Container maxW="container.lg" py={8}>
        <Outlet />
      </Container>
    </Box>
  );
}
