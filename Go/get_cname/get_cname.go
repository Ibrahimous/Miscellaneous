package main

import (
    "io"
    "net"
    "net/http"
    "os"
    "archive/zip"
    "fmt"
    "log"
    "path/filepath"
    "strings"
    "regexp"
    "encoding/csv"
)

func log_fatal(err error) {
    if err != nil {
        log.Fatal(err)
    }
}

func main() {

	//Get Alexa top 1M sites
    fileUrl := "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
    err := DownloadFile("top-1m.csv.zip", fileUrl)
    log_fatal(err)

    //Unzip that file to the output directory
    files, err := Unzip("top-1m.csv.zip", "output")
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("Unzipped: " + strings.Join(files, ", "))

    //Parse the unzipped file and returns the CNAMES matching *.cloudfront.net
    parse_csv("output/top-1m.csv")
}

// DownloadFile will download a url to a local file. It's efficient because it will
// write as it downloads and not load the whole file into memory.
func DownloadFile(filepath string, url string) error {

    // Create the file
    out, err := os.Create(filepath)
    if err != nil {
        return err
    }
    defer out.Close()

    // Get the data
    resp, err := http.Get(url)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    // Write the body to file
    _, err = io.Copy(out, resp.Body)
    if err != nil {
        return err
    }

    return nil
}

// Unzip will un-compress a zip archive,
// moving all files and folders to an output directory
func Unzip(src, dest string) ([]string, error) {

    var filenames []string

    r, err := zip.OpenReader(src)
    if err != nil {
        return filenames, err
    }
    defer r.Close()

    for _, f := range r.File {

        rc, err := f.Open()
        if err != nil {
            return filenames, err
        }
        defer rc.Close()

        // Store filename/path for returning and using later on
        fpath := filepath.Join(dest, f.Name)
        filenames = append(filenames, fpath)

        if f.FileInfo().IsDir() {

            // Make Folder
            os.MkdirAll(fpath, os.ModePerm)

        } else {

            // Make File
            var fdir string
            if lastIndex := strings.LastIndex(fpath, string(os.PathSeparator)); lastIndex > -1 {
                fdir = fpath[:lastIndex]
            }

            err = os.MkdirAll(fdir, os.ModePerm)
            if err != nil {
                log.Fatal(err)
                return filenames, err
            }
            f, err := os.OpenFile(
                fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
            if err != nil {
                return filenames, err
            }
            defer f.Close()

            _, err = io.Copy(f, rc)
            if err != nil {
                return filenames, err
            }

        }
    }
    return filenames, nil
}

func parse_csv(filename string) {
	/*
	TODO: compare with previous results to avoid too many dns requests
	*/

    // Open CSV file
    f, err := os.Open(filename)
    log_fatal(err)
    defer f.Close()

    // Read File into a Variable
    lines, err := csv.NewReader(f).ReadAll()
    log_fatal(err)
    valid_cname := regexp.MustCompile(`^[a-z0-9]+\.cloudfront\.net\.?$`)

    // Loop through lines & turn into object
    for _, line := range lines {
        /*data := CsvLine{
            Column1: line[0],
            Column2: line[1],
        }
        fmt.Println(data.Column1 + " " + data.Column2)*/
        //fmt.Println("Im gonna lookup:", line[1])
        
	    //Linux "dig domain.com CNAME "equivalent
	    /*
	    https://idea.popcount.org/2013-11-28-how-to-resolve-a-million-domains/
	    go get github.com/majek/goplayground/resolve
	    echo -en "google.com\nfacebook.com\nwikipedia.org\n" | $GOPATH/bin/resolve -server="8.8.8.8:53"
	    => complicated
	    */
        cname, err := net.LookupCNAME(line[1])
        //log_fatal(err)
        if err != nil {}
        if valid_cname.MatchString(cname) {
        	fmt.Println(line[1], cname)
        }
    }
}
