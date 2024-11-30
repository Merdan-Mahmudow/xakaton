import {
  Avatar,
  Box,
  Button,
  Container,
  Flex,
  Icon,
  useBreakpointValue,
  useColorMode,
  useColorModeValue,
  Textarea,
  Select,
  IconButton,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import useAuth from "../../hooks/useAuth";
import { useEffect, useRef, useState } from "react";
import { FaPaperPlane } from "react-icons/fa";
import { useMutation } from "@tanstack/react-query";
import {
  type YandexGPTRequest,
  type TDataYandexGPTRequest,
  TDataGigaChatRequest,
  GigaChatRequest,
} from "../../client";
import { useQueryClient } from "@tanstack/react-query"
import type { UserPublic } from "../../client"
import {
	RiDeleteBinLine, // Import delete icon
  } from "react-icons/ri"; // Assuming you're using react-icons

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
});

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
}

function Dashboard() {
  const { yagptRequest } = useAuth();
  const { gigachatRequest } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const { colorMode } = useColorMode();
  const isDarkMode = colorMode === "dark";
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [selectedModel, setSelectedModel] = useState<string>("yagpt"); // Default to yagpt

  let mutation: any;

  if (selectedModel === "yagpt") {
    mutation = useMutation({
      mutationFn: async (data: TDataYandexGPTRequest) => {
        return await yagptRequest(data);
      },
      onSuccess: (response: YandexGPTRequest) => {
        const assistantResponse: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          text: response.text,
        };
        setMessages((prevMessages) => [...prevMessages, assistantResponse]);
        updateLocalStorage("yagpt", assistantResponse);
      },
      onError: (error) => {
        console.error("Ошибка при запросе к API:", error);
      },
    });
  } else if (selectedModel === "gigachat") {
    mutation = useMutation({
      mutationFn: async (data: TDataGigaChatRequest) => {
        return await gigachatRequest(data);
      },
      onSuccess: (response: GigaChatRequest) => {
        const assistantResponse: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          text: response.content,
        };
        setMessages((prevMessages) => [...prevMessages, assistantResponse]);
        updateLocalStorage("gigachat", assistantResponse);
      },
      onError: (error) => {
        console.error("Ошибка при запросе к API:", error);
      },
    });
  }

  const sendMessage = async () => {
    if (inputMessage.trim() === "") return;

    const newMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      text: inputMessage,
    };

    await setMessages((prevMessages) => [...prevMessages, newMessage]);
	const updatedMessages = [...messages, newMessage];
    setInputMessage("");
    updateLocalStorage(selectedModel, newMessage); // Update localStorage with user message

    const requestData =
      selectedModel === "yagpt"
        ? {
            prompt: updatedMessages.map((message) => ({
              role: message.role,
              text: message.text,
            })),
            stream: false,
          }
        : {
            messages: updatedMessages.map((message) => ({
              role: message.role,
              content: message.text,
            })),
          };

   await mutation.mutateAsync(requestData);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Load messages from localStorage based on selectedModel
  useEffect(() => {
    const storedMessages = localStorage.getItem("messages");
    if (storedMessages) {
      const parsedMessages = JSON.parse(storedMessages);
      setMessages(parsedMessages[selectedModel] || []);
    }
  }, [selectedModel]);

  const isMobile = useBreakpointValue({ base: true, md: false });

  const textColor = useColorModeValue("gray.800", "gray.100");
  const inputBg = useColorModeValue("white", "gray.700");
  const messageBgUser = useColorModeValue("teal.500", "teal.700");
  const messageBgAssistant = useColorModeValue("gray.200", "gray.600");

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 10 + "px";
      textareaRef.current.style.height =
        textareaRef.current.scrollHeight + "px";
    }
  }, [inputMessage]);

  // Function to update localStorage
  const updateLocalStorage = (model: string, message: ChatMessage) => {
    const storedMessages = localStorage.getItem("messages") || "{}";
    const parsedMessages = JSON.parse(storedMessages);
    parsedMessages[model] = parsedMessages[model] || []; // Initialize if it doesn't exist
    parsedMessages[model].push(message);
    localStorage.setItem("messages", JSON.stringify(parsedMessages));
  };

  // Function to clear chat history for the selected model
  const clearChatHistory = () => {
    // Update localStorage, removing messages for the selected model
    const storedMessages = localStorage.getItem("messages") || "{}";
    const parsedMessages = JSON.parse(storedMessages);
    parsedMessages[selectedModel] = []; // Clear messages for the selected model
    localStorage.setItem("messages", JSON.stringify(parsedMessages));

    // Clear the messages in the state
    setMessages([]);
  };

  return (
    <Container
      maxW={isMobile ? "full" : "container.xl"}
      h="calc(100vh - 20px)"
      pt={20}
      px={0}
    >
      <Flex
        justifyContent="space-between"
        alignItems="center"
        top={3.5}
        left={"50%"}
        transform={"translateX(-50%)"}
        position={"fixed"}
        px={4}
        maxW={"fit-content"}
      >
        <Select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
        >
          <option value="yagpt">YandexGPT</option>
          <option value="gigachat">GigaChat</option>
          {/* Add more model options as needed */}
        </Select>
		<IconButton
          aria-label="Clear chat history"
          icon={<RiDeleteBinLine />}
          onClick={clearChatHistory}
          ml={2} // Add some margin to the left
        />
      </Flex>
      <Flex direction="column" h="full" align="stretch">
        <Box
          flex="1"
          overflowY="auto"
          p={4}
          borderRadius="md"
          ref={chatContainerRef}
          sx={{
            "&::-webkit-scrollbar": {
              width: "8px",
            },
            "&::-webkit-scrollbar-track": {
              background: "transparent",
            },
            "&::-webkit-scrollbar-thumb": {
              background: isDarkMode ? "gray.600" : "gray.300",
              borderRadius: "4px",
            },
            "&::-webkit-scrollbar-thumb:hover": {
              background: isDarkMode ? "gray.500" : "gray.400",
            },
          }}
        >
          {messages.map((message) => (
            <ChatMessageItem
              key={message.id}
              message={message}
              isUser={message.role === "user"}
              messageBgUser={messageBgUser}
              messageBgAssistant={messageBgAssistant}
            />
          ))}
        </Box>

        <Flex mt={4} align="center" mx={10}>
          <Textarea
            minBlockSize={isMobile ? "20px" : "20px"}
            maxBlockSize={isMobile ? "100px" : "150px"}
            ref={textareaRef}
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            mr={2}
            py={3}
            borderRadius="md"
            borderTopLeftRadius="full"
            borderBottomLeftRadius="full"
            bg={inputBg}
            color={textColor}
            resize="none"
          />
          <Button
            type="submit"
            onClick={sendMessage}
            colorScheme="teal"
            borderRadius="md"
          >
            <Icon as={FaPaperPlane} />
          </Button>
        </Flex>
      </Flex>
    </Container>
  );
}

function ChatMessageItem({
  message,
  isUser,
  messageBgUser,
//  messageBgAssistant,
}: {
  message: ChatMessage;
  isUser: boolean;
  messageBgUser: string;
  messageBgAssistant: string;
}) {
	const { colorMode } = useColorMode();
	const isDarkMode = colorMode === "dark";
	const queryClient = useQueryClient()
	const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])
  return (
    <Flex
      mb={3}
      justifyContent={isUser ? "flex-end" : "flex-start"}
      alignItems="flex-start"
    >
      {!isUser && (
        <Avatar name="ChatGPT" size="sm" mr={2} bg="teal.500" color="white" />
      )}
      <Box
        bg={isUser ? messageBgUser : "transparent"}
        color={isDarkMode ? "white" : isUser ? "white": "black"}
        p={3}
		borderTop={isUser ? "none" : "1px"}
		borderColor={isDarkMode ? "white" : isUser ? "white": "black"}
		borderRadius={isUser ? "full" : "none"}
      >
        {message.text}
      </Box>
      {isUser && (
        <Avatar src={currentUser?.avatar ? currentUser?.avatar : undefined} size="sm" ml={2}/>
      )}
    </Flex>
  );
}

export default Dashboard;

