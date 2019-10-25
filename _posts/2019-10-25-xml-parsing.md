---
layout: post
title: XML parsing in Rust
---

Did I think that XML was dead? Well, I was wrong: it isn't. XML is here to stay with us forever. Let's see how I parsed some XML with Rust.

The library that seems the right tool for the job is [serde-xml-rs](https://github.com/RReverser/serde-xml-rs). Like the name suggests, it will parse an XML file and leverage Serde for the serialization.

Let's say we have this file (examples from the crate's documentation).

``` xml
<Project name="my_project">
    <Item name="hello" source="world.rs" />
</Project>
```

Let's parse it using an XML library that leverages serde into our own Struct:

``` rust
#[derive(Debug, Deserialize)]
struct Project {
    pub name: String,
    #[serde(rename = "Item", default)]
    pub items: Vec<Item>,
}
```

Basic usage, load the whole XML file in memory and parse it:

``` rust
let s = "project.xml";
let f = File::open(s).expect(&format!("Cannot open file {}", s));
let r = BufReader::new(f);
let prj: Project = serde_xml_rs::de::from_reader(r).unwrap();
println!("{:?}", prj);
```

Note: like noted in the [Rust documentation](https://doc.rust-lang.org/std/io/struct.BufReader.html), in this specific case using a buffered reader (`std::io::BufReader`) does not offer significant advantages.

The output will be:

``` bash
$ cargo run
....
Project { name: "my_project", items: [Item { name: "hello", source: "world.rs" }] }
```

In my case I had a [chunked body response](https://docs.rs/hyper/0.12.33/hyper/struct.Body.html) received from a Hyper Future so I need to jump through more hoops (I suspect I can improve on this).

``` rust
use serde_xml_rs::from_reader;

// Hyper::Chunk -> Bytes -> &str
let b = body.into_bytes();
let xml_str = str::from_utf8(&b).unwrap();

// deserialize the slice into a Project
let project: Project = serde_xml_rs::from_str(xml_str).unwrap();
```

Now, parsing with serde sometimes is boring. When the parsing fails error messages are not always useful.

Let's add [Serde path to error](https://github.com/dtolnay/path-to-error) to the recipe: a crate that tries to point you where exactly the parsing fails.

``` rust
...

// create an instance of the deserializer suitable for serde_path_to_error
let jd = &mut serde_xml_rs::de::Deserializer::new(r);
let result: Result<Project, _> = serde_path_to_error::deserialize(jd);
if let Err(err) = result {
    let path = err.path().to_string();
    panic!("Could not deserialize at: {}", path);
}
```

So the final result would look like something like this:

``` rust
let s = "project.xml";
let f = File::open(s).expect(&format!("Cannot open file {}", s));
let r = BufReader::new(f);
let jd = &mut serde_xml_rs::de::Deserializer::new_from_reader(r);
let result: Result<Project, _> = serde_path_to_error::deserialize(jd);
assert_eq!(result.is_ok());
```

Warning: `serde_xml` has some limitations. For example one thing that bit me is that it does not parse [XML tags with namespaces](https://github.com/RReverser/serde-xml-rs/issues/64). That could be a serious limitation in some contexts.

### <a id="part_3" href="#part_3" class="header-anchor"># </a>Closing thoughts

Parsing XML is ugly because XML tried (and failed) to conquer the world. So it has been filled with all kind of extensions and shit.

I wouldn't say that Rust is the ideal tool for parsing XML, other languages (and libraries) can run circles around this tool I've tried, but what I gain here is an implicit and strict type-checking of the XML parsed.

In the end, after playing a bit with all this, I just dumped everything and used the [rss](https://docs.rs/rss/1.8.0/rss) crate, since all I had to do was parsing a RSS feed (lol).
