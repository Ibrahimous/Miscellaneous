#/usr/bin/bash
# See Miscellaneous/Go/install_golang.sh for installing golang
whereis go
#go: /usr/bin/go /usr/lib/x86_64-linux-gnu/go /home/linuxbrew/.linuxbrew/bin/go /usr/share/man/man1/go.1.gz
go version
#go version go1.21.6 linux/amd64

echo $GOPATH
#/home/charlou/Go
echo $GOROOT
#NULL

go install github.com/99designs/gqlgen@latest
printf '// +build tools\npackage tools\nimport _ "github.com/99designs/gqlgen"' | gofmt > tools.go
#go mod tidy
#go: go.mod file not found in current directory or any parent directory; see 'go help modules'

go mod init github.com/Ibrahimous/Miscellaneous/tree/master/Go/GraphQL_projects
go mod tidy
go run github.com/99designs/gqlgen init
go run ./server.go
