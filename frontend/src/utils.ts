import type { ApiError } from "./client"

export const emailPattern = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Неправильная почта",
}

export const namePattern = {
  value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
  message: "Неправильное имя",
}

export const passwordRules = (isRequired = true) => {
  const rules: any = {
    minLength: {
      value: 8,
      message: "Пароль должен содержать не менее 8 символов",
    }
  }

  if (isRequired) {
    rules.required = "Обязательно для заполнения"
  }

  return rules
}

export const confirmPasswordRules = (
  getValues: () => any,
  isRequired = true,
) => {
  const rules: any = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password
      return value === password ? true : "Пароли не совпадают"
    },
  }

  if (isRequired) {
    rules.required = "Подтверждение пароля обязательно"
  }

  return rules
}

export const handleError = (err: ApiError, showToast: any) => {
  const errDetail = (err.body as any)?.detail
  let errorMessage = errDetail || "Что-то пошло не так."
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    errorMessage = errDetail[0].msg
  }
  showToast("Ошибка", errorMessage, "error")
}
