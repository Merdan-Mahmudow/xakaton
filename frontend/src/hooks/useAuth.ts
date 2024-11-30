import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";

import { AxiosError } from "axios";
import {
  type Body_login_login_access_token as AccessToken,
  type ApiError,
  ImageGenerationService,
  ItemsService,
  LoginService,
  type UserPublic,
  type UserRegister,
  UsersService,
  YandexARTGetRequest,
  YandexARTRequest,
} from "../client";
import useCustomToast from "./useCustomToast";

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null;
};

const useAuth = () => {
  const [error, setError] = useState<string | null>(null);
  const [imageID, setImageID] = useState<string>("");
  const [imageURL, setImageURL] = useState<string | null>(null);
  const navigate = useNavigate();
  const showToast = useCustomToast();
  const queryClient = useQueryClient();
  const { data: user, isLoading } = useQuery<UserPublic | null, Error>({
    queryKey: ["currentUser"],
    queryFn: UsersService.readUserMe,
    enabled: isLoggedIn(),
  });

  const signUpMutation = useMutation({
    mutationFn: (data: UserRegister) =>
      UsersService.registerUser({ requestBody: data }),

    onSuccess: () => {
      navigate({ to: "/login" });
      showToast(
        "Account created.",
        "Your account has been created successfully.",
        "success"
      );
    },
    onError: (err: ApiError) => {
      let errDetail = (err.body as any)?.detail;

      if (err instanceof AxiosError) {
        errDetail = err.message;
      }

      showToast("Something went wrong.", errDetail, "error");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    });
    localStorage.setItem("access_token", response.access_token);
  };

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      navigate({ to: "/" });
    },
    onError: (err: ApiError) => {
      let errDetail = (err.body as any)?.detail;

      if (err instanceof AxiosError) {
        errDetail = err.message;
      }

      if (Array.isArray(errDetail)) {
        errDetail = "Something went wrong";
      }

      setError(errDetail);
    },
  });

  const logout = () => {
    localStorage.removeItem("access_token");
    navigate({ to: "/login" });
  };

  const yaArtPostMutation = useMutation({
    mutationFn: async (prompt: YandexARTRequest) =>
      await ImageGenerationService.YandexARTGeneration(prompt),
    onSuccess: (data: any) => {
      setImageID(data[1].id);
      showToast(
        "Генерация изображения",
        "Ваше запрос отправлен на обработку",
        "success"
      );
    },
  });
  const yaArtGetMutation = useMutation({
    mutationFn: async (id: YandexARTGetRequest) =>
      await ImageGenerationService.YandexARTGet(id),
    onSuccess: (data: any) => {
      setImageURL(data);
      showToast("Генерация изображения", "Ваше изображение готово", "success");
    },
  });
  const updateLocalStorage = (newImage: string) => {
    const storedImages = localStorage.getItem("generatedImages") || "[]";
    const parsedImages = JSON.parse(storedImages);
    if (newImage){
		localStorage.setItem(
			"generatedImages",
			JSON.stringify([...parsedImages, newImage])
		  );
	}
  };
  const YaARTRequest = async (prompt: YandexARTRequest) => {
	try {
		// 1. Get the image ID from the post mutation
		const imageIdResponse = await yaArtPostMutation.mutateAsync(prompt);
		setImageID(imageIdResponse[1].id); // Update imageID state
  
		// 2. Use the received image ID to fetch the image URL
		const imageUrlResponse = await yaArtGetMutation.mutateAsync({ id: imageIdResponse[1].id });
		setImageURL(imageUrlResponse); // Update imageURL state
  
		// 3. Update localStorage with the fetched image URL
		updateLocalStorage(imageUrlResponse);
  
		// 4. Optionally return the image URL for immediate use
		return imageUrlResponse; 
	  } catch (error) {
		console.error("Image generation process failed:", error);
		// Handle the error appropriately (e.g., show an error toast)
		return null; 
	  }
  };

  const yagptRequest = async (prompt: any) => {
    const response = await ItemsService.yagptRequest({
      prompt: prompt,
      stream: false,
    });
    return response;
  };

  const gigachatRequest = async (messages: any) => {
    const response = await ItemsService.gigachatRequest({
      prompt: messages,
    });
    return response;
  };
  return {
	imageID,
	imageURL,
    signUpMutation,
    loginMutation,
    logout,
    user,
    isLoading,
    error,
    YaARTRequest,
    yagptRequest,
    gigachatRequest,
    resetError: () => setError(null),
  };
};

export { isLoggedIn };
export default useAuth;
