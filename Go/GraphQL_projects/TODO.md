https://www.apollographql.com/blog/using-graphql-with-golang

charlou@PC-Imothep:~/DEV/Miscellaneous/Go/GraphQL_projects$ go help install
usage: go install [build flags] [packages]
...
Executables are installed in the directory named by the GOBIN environment
variable, which defaults to $GOPATH/bin or $HOME/go/bin if the GOPATH
environment variable is not set. Executables in $GOROOT
are installed in $GOROOT/bin or $GOTOOLDIR instead of $GOBIN.

...


https://the-guild.dev/blog/graphql-deep-dive-1
->
Introduction to GraphQL - Learn about GraphQL, how it works, and how to use it
How to GraphQL - The Fullstack Tutorial for GraphQLThe free and open-source tutorial to learn all around GraphQL to go from zero to production
Explore GraphQL - This is your GraphQL study guide. Learn the fundamentals of schemas and queries, then implement some apps
GraphQL Tutorial - GraphQL is becoming the new way to use APIs in modern web and mobile apps. However, learning new things always takes
GraphQL Concepts Visualized - GraphQL is often explained as a "unified interface to access data from different sources"

#TODO

https://www.apollographql.com/blog/using-graphql-with-golang#defining-the-backend-to-fetch-and-store-values

Quick explanations:
In server.go, the following line:
	`srv := handler.NewDefaultServer(graph.NewExecutableSchema(graph.Config{Resolvers: &graph.Resolver{}}))`
1. Use the handler's `NewDefaultServer` function defined (here)[https://github.com/99designs/gqlgen/blob/master/graphql/handler/server.go]
2. ... to run the `NewExecutableSchema` function defined on your local BUT auto-generated `generated.go`
3. ... with config graph.Config{Resolvers: &graph.Resolver{}} - where is &graph.Resolver{} = an actual instance of ResolverRoot????


#ALIRE
For more about build flags, see 'go help build'.
For more about specifying packages, see 'go help packages'.
See also: go build, go get, go clean.

------------------

https://www.apollographql.com/docs/apollo-server/schema/schema
https://ivan-corrales-solera.medium.com/dive-into-graphql-9bfedf22e1a
