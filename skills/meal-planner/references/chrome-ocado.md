# Chrome + Ocado receipt download

## Overview
The Ocado receipt email contains a link to view/download the receipt as a PDF on the Ocado
website. The user must be logged in to Ocado for this to work. Claude in Chrome navigates
to the link and extracts the receipt content.

## Step-by-step

### 1. Extract the URL from the Gmail thread
The receipt email from ocado@ocado.com typically contains a button or link labelled one of:
- "View your receipt"
- "Download receipt"
- "See your order"

Extract the raw href from the email HTML. It will look something like:
`https://www.ocado.com/webshop/receipt?orderId=XXXXXXXXX`

### 2. Navigate in Chrome
```
navigate(url=<receipt_url>)
```

### 3. Handle login if required
If the page redirects to a login screen:
- Stop and inform the user: "The Ocado page requires you to be logged in. Please log in to
  Ocado in Chrome and then let me know to continue."
- Wait for confirmation before proceeding.
- Do NOT attempt to enter login credentials.

### 4. Extract receipt content
Once on the receipt page, use one of:
- `get_page_text()` — if the receipt is rendered as HTML text on the page
- If a PDF is displayed inline in the browser, use `get_page_text()` on the PDF viewer — 
  Chrome's built-in PDF viewer exposes text content this way
- If there is a "Download PDF" button, use `find()` to locate it, then note the download URL
  and ask the user for explicit permission before downloading:
  > "I found a download button for [filename]. Shall I download it?"

### 5. Parse the extracted text
The receipt text will contain sections including:
- Order number and delivery date
- Cost summary (ignore for meal planning)
- **Fridge** section — items with use-by dates grouped by date
- **Cupboard** section — longer-life items
- **Offers savings** section (ignore for meal planning)

Focus parsing on the Fridge and Cupboard sections. For each line item extract:
- Product name (strip brand prefix if unhelpful, e.g. "M&S", "Ocado")
- Use-by grouping (the receipt uses headers like "Use by end of Wednesday")
- Quantity delivered (the X/Y delivered format — use the left number)

## Fallback if Chrome is unavailable
If Claude in Chrome tools are not available in the current session:
1. Ask the user to forward the Ocado receipt email to themselves and paste the plain-text
   content into the chat
2. Or ask them to upload the PDF directly as a file attachment
3. Parse from whatever format is provided
