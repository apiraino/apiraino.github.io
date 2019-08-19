---
layout: post
title: Getting into Rust Iterators
---

I'll summarize what I've learned so far about Iterators.

I had this code:
``` rust
pub fn mapper(src: &Vec<SrcStruct>) -> Vec<DestStruct> {
    let mut objects: Vec<DestStruct> = vec![];
    for course in src {
        let item = Item::from(course);
        let obj: DestStruct = DestStruct::new(item);
        objects.push(obj);
    }
    objects
}
```

This function takes as input an array of <strong>Srcstruct</strong> references and return an array of <strong>DestStruct</strong>. For each item of <strong>SrcStruct</strong> we create a new <strong>Deststruct</strong> and add it to the array. At the end of the iteration the array is returned.

That's a pretty straightforwarded approach, which works well in most cases and looks familiar in most languages. Nobody will complain about such implementation.

However what happens when the input array is a HUUUGE amount of data?

Iterators save the day, providing a way to stream data and be treated chunk by chunk. Since my input data is basically a JSON list of records, it look like the perfect use case for iterating them one by one and keep memory usage constant.

The first refactor tries to add Interators:
``` rust
pub fn mapper<'a, I>(src: I) -> impl Iterator<Item = DestStruct>
where
    I: IntoIterator<Item = &'a SrcStruct>,
{
    let objects: Vec<DestStruct> = src
        .into_iter()
        .map(|course| {
            let res = Item::try_from(course);
            let item = match res {
                Ok(item) => {
                    // conversion successful
                    item
                }
                Err(x) => {
                    // conversion failed! Create a placeholder
                    Item::default()
                }
            };
            DestStruct::new(item)
        })
        .collect();
    objects.into_iter()
}
```


The final version looks like this:

``` rust
pub fn mapper<'a, I>(src: I) -> impl Iterator<Item = ApprendoObject> + 'a
where
    I: IntoIterator<Item = &'a CourseResult>,
    <I as std::iter::IntoIterator>::IntoIter: 'a,
{
    let objects = src.into_iter().map(|course| {
        let res = Item::try_from(course);
        let item = match res {
            Ok(item) => {
                debug!("conversion for object successful");
                item
            }
            Err(x) => {
                error!("conversion for object failed: {:?}", x);
                // and skip this object
                let empty_item = Item::default();
                empty_item
            }
        };
        let app_obj: ApprendoObject = ApprendoObject::new(item);
        app_obj
    });
    objects
}
```

I'd like to run some benchmarks on these two implementations (although benchmarks are like opinions: everyone has their own); unfortunately I could not figure out easily how to run benchmarks in Rust, so I'll leave a <strong>cargo bench</strong> setup for a later stage.
