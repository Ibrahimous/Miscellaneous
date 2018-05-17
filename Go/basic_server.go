package main

import (
	//"io/ioutil"
	"net/http"
	"fmt"
	//"bytes"
	"strings"
	"io"
	"os"
	"log"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

/*
func saveHandler(w http.ResponseWriter, r *http.Request) {
    //title := r.URL.Path[len("/save/"):]
    body := r.FormValue("body")
	fmt.Println(body)
	err := ioutil.WriteFile("file.txt", []byte(body), 0644)
	check(err)
}
*/

//https://stackoverflow.com/questions/40684307/how-can-i-receive-an-uploaded-file-using-a-golang-net-http-server
//curl http://localhost:8080/upload -F "fileupload=@test.txt" -vvv
func ReceiveFile(w http.ResponseWriter, r *http.Request) {
    //var Buf bytes.Buffer
    fmt.Println("Entering ReceiveFile")
    srcFile, header, err := r.FormFile("fileupload")
    if err != nil {
    	fmt.Println("File upload failed")
        panic(err)
    }
    defer srcFile.Close()
    name := strings.Split(header.Filename, ".")
    fmt.Printf("File name %s\n", name[0])
    /*
    // Copy the file data to my buffer
    io.Copy(&Buf, file)
    // do something with the contents...
    // I normally have a struct defined and unmarshal into a struct, but this will
    // work as an example
    contents := Buf.String()
    fmt.Println(contents)
    // I reset the buffer in case I want to use it again
    // reduces memory allocations in more intense projects
    Buf.Reset()
    // do something else
    // etc write header
    */
	

	//err1 := ioutil.WriteFile(name, file, 0644)
	//check(err1)

	dstFile, err := os.Create("dstfile.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer dstFile.Close()

	_, err = io.Copy(dstFile, srcFile)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	http.HandleFunc("/save/", ReceiveFile)
	http.ListenAndServe(":8000", nil)
}
