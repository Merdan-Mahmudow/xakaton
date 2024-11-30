import {
  Box,
  Button,
  Container,
//  Flex,
  Grid,
  Heading,
  Image,
  Input,
  Stack,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import useAuth from "../../hooks/useAuth";

export const Route = createFileRoute("/_layout/images")({
  component: Images,
});

function Images() {
  const [generatedImages, setGeneratedImages] = useState<string[]>([]);
  const [inputPrompt, setInputPrompt] = useState<string>("");
  const { YaARTRequest } = useAuth();
  const handleGenerateImage = async () => {
    try {
      await YaARTRequest({ prompt: inputPrompt });
    } catch (error) {
      console.error("error", error);
    }
  };

  //  const updateLocalStorage = (newImage: string) => {
  //    const storedImages = localStorage.getItem("generatedImages") || "[]";
  //    const parsedImages = JSON.parse(storedImages);
  //    localStorage.setItem(
  //      "generatedImages",
  //      JSON.stringify([...parsedImages, newImage])
  //    );
  //  };

  useEffect(() => {
    const storedImages = localStorage.getItem("generatedImages");
    if (storedImages) {
      setGeneratedImages(JSON.parse(storedImages));
    }
  }, [generatedImages]);

  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} py={12}>
        Image Generation
      </Heading>
      <Stack direction="row" spacing={4} mb={4}>
        <Input
          type="text"
          placeholder="Enter image prompt..."
          value={inputPrompt}
          onChange={(e) => setInputPrompt(e.target.value)}
        />
        <Button colorScheme="teal" onClick={handleGenerateImage}>
          Generate
        </Button>
      </Stack>
      <Grid templateColumns="repeat( auto-fit, minmax(200px, 1fr) )" gap={2}>
        {generatedImages.reverse().map((url, index) => (
          <Box key={index} w="200px" borderRadius={10} overflow="hidden">
            <Image src={url} alt={`Generated image ${index + 1}`} />
          </Box>
        ))}
      </Grid>
    </Container>
  );
}

export default Images;
