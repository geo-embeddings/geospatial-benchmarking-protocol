import { Box, Container, Flex, HStack, IconButton, Image } from "@chakra-ui/react";
import { LuMoon, LuSun } from "react-icons/lu";
import { Link, Outlet } from "react-router";
import { useColorMode } from "../use-color-mode";

export default function Layout() {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Box minH="100vh">
      <Box as="nav" bg="brand.600" color="white" py={3} px={4}>
        <Container maxW="container.lg">
          <Flex justify="space-between" align="center">
            <Link to="/">
              <HStack>
                <Image src="/gbp-logo.svg" alt="GBP" height="32px" />
                GBP
              </HStack>
            </Link>
            <HStack gap={6}>
              <Link to="/datasets">Datasets</Link>
              <Link to="/results">Results</Link>
              <IconButton
                size="xs"
                variant="ghost"
                color="white"
                onClick={toggleColorMode}
                aria-label="Toggle color mode"
              >
                {colorMode === "light" ? <LuMoon /> : <LuSun />}
              </IconButton>
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
