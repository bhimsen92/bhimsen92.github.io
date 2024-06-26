---
title: 'Learning Scala'
date: 2023-01-27T22:50:00+05:30
tags:
  - scala
---

In the [previous post]({{< ref "/how-to-learn-new-programming-language-quickly" >}}) we came up with the template for learning a new language. In this post we will use it to learn [Scala](https://www.scala-lang.org).

## Build and Dependency Management

sbt is a build and dependency management tool for Scala. If your project is managed by sbt, then your folder structure should be organised as follows:

```
build.sbt
project/
  *.scala files
src/
  main/
    resources/
    scala/
  test/
    resources/
    scala/
```

sbt needs a build definition file called `build.sbt`. To support the build process, you can also keep scala files inside `project/*.scala` files. sbt combines both `build.sbt` and files inside `projects/` to build your project.

sbt relies on two things: tasks and settings. Task defines the action that you want to perform and setting defines key/value pair that will be used by the tasks.

Some example tasks include: `sbt compile, sbt clean, sbt run, sbt test sbt console`. To get all the tasks applicable for the project, please execute sbt tasks.

you can execute sbt tasks via command line or get into an interactive mode by executing "sbt" and then invoking the tasks one by one. Interactive mode is helpful if you want to test your application. Because it loads all the files and puts them in the classpath.

A sample build.sbt file:

```scala
// key-value pairs.
name := "scala-project"
version := "1.0.0"
scalaVersion := "2.11.6"

// define dependencies.
libraryDependencies = Seq(
"org.scalatest" % "scalatest_2.11" % "2.2.6" % "test"
)
```

libraryDependency follows this pattern: `libraryDependencies = Seq(groupID % artifactID % version % configuration)`

configuration is not needed for all artefacts but test artefacts need `"test"` configuration.

you can add compile option in sbt like this:
`scalacOptions ++= Seq("-feature", "-language:\_", "-unchecked", "-deprecation", "-encoding", "utf8")`

The last thing that I want to mention is plugins. Plugins are basically user defined tasks which you can add to your project. Some example plugins are `sbt-scalafmt` for formatting your code. all plugins should be defined inside the `project/plugins.sbt` file.

you can find the needed dependency artefacts here: [MVN Repository](https://mvnrepository.com)

more information about sbt can be found here: [More on sbt](https://www.scala-sbt.org/1.x/docs/sbt-by-example.html)