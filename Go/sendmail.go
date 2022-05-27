//reference: https://developers.google.com/gmail/api/quickstart/go & https://github.com/xDinomode/Go-Gmail-Api-Example/blob/master/email.go

package main

import (
        "encoding/json"
        "encoding/base64"

        "fmt"
        "io/ioutil"
        "log"
        "net/http"
        "os"

        "golang.org/x/net/context"
        "golang.org/x/oauth2"
        "golang.org/x/oauth2/google"
        "google.golang.org/api/gmail/v1"
)

// Retrieve a token, saves the token, then returns the generated client.
func getClient(config *oauth2.Config) *http.Client {
        // The file token.json stores the user's access and refresh tokens, and is
        // created automatically when the authorization flow completes for the first
        // time.
        tokFile := "token.json"
        tok, err := tokenFromFile(tokFile)
        if err != nil {
                tok = getTokenFromWeb(config)
                saveToken(tokFile, tok)
        }
        return config.Client(context.Background(), tok)
}

// Request a token from the web, then returns the retrieved token.
func getTokenFromWeb(config *oauth2.Config) *oauth2.Token {
        authURL := config.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
        fmt.Printf("Go to the following link in your browser then type the "+
                "authorization code: \n%v\n", authURL)

        var authCode string
        if _, err := fmt.Scan(&authCode); err != nil {
                log.Fatalf("Unable to read authorization code: %v", err)
        }

        tok, err := config.Exchange(context.TODO(), authCode)
        if err != nil {
                log.Fatalf("Unable to retrieve token from web: %v", err)
        }
        return tok
}

// Retrieves a token from a local file.
func tokenFromFile(file string) (*oauth2.Token, error) {
        f, err := os.Open(file)
        if err != nil {
                return nil, err
        }
        defer f.Close()
        tok := &oauth2.Token{}
        err = json.NewDecoder(f).Decode(tok)
        return tok, err
}

// Saves a token to a file path.
func saveToken(path string, token *oauth2.Token) {
        fmt.Printf("Saving credential file to: %s\n", path)
        f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0600)
        if err != nil {
                log.Fatalf("Unable to cache oauth token: %v", err)
        }
        defer f.Close()
        json.NewEncoder(f).Encode(token)
}

func main() {
        b, err := ioutil.ReadFile("credentials.json")
        if err != nil {
                log.Fatalf("Unable to read client secret file: %v", err)
        }

        // If modifying these scopes, delete your previously saved token.json.
        // https://developers.google.com/gmail/api/auth/scopes
        config, err := google.ConfigFromJSON(b, gmail.GmailSendScope)
        if err != nil {
                log.Fatalf("Unable to parse client secret file to config: %v", err)
        }
        client := getClient(config)

        srv, err := gmail.New(client)
        if err != nil {
                log.Fatalf("Unable to retrieve Gmail client: %v", err)
        }

        // New message for our gmail service to send
        var message gmail.Message

        usersList := []string{"rachid", "momo"}

        for i, u := range usersList {

                fmt.Printf("Sending to user %i\r\n", i)

                // Compose the message
                messageStr := []byte(
                        "From: <your mail here>\r\n" +
                        "To: "+u+"@<yourTargetCorporationHere>\r\n" +
                        "Subject: My third Gmail API message\r\n\r\n" +
                        "yourBodyHere")

                // Place messageStr into message.Raw in base64 encoded format
                message.Raw = base64.URLEncoding.EncodeToString(messageStr)

                // Send the message
                _, err = srv.Users.Messages.Send("me", &message).Do()
                if err != nil {
                        log.Printf("Error: %v", err)
                } else {
                        fmt.Printf("Message to %s sent!\r\n", u)
               }
       }
}
