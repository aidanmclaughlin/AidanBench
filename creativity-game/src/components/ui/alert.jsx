import React from "react"

export const Alert = ({ children, className = "", ...props }) => (
  <div
    role="alert"
    className={`rounded-lg border border-gray-200 p-4 ${className}`}
    {...props}
  >
    {children}
  </div>
)

export const AlertTitle = ({ children, className = "", ...props }) => (
  <h5
    className={`mb-1 font-medium leading-none tracking-tight ${className}`}
    {...props}
  >
    {children}
  </h5>
)

export const AlertDescription = ({ children, className = "", ...props }) => (
  <div
    className={`text-sm [&_p]:leading-relaxed ${className}`}
    {...props}
  >
    {children}
  </div>
)
