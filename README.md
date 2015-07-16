# Multiverse JSON

a lightweight specification for storing alternate versions of a document using JSON

# What is this?

Writing existing as structured data instead of static text strings should in theory allow the content to be reused and repurposed without being rewritten or extensively edited. **Multiverse JSON** is an attempt to *store* linear writing in a *single nonlinear format*, such that it can be *compiled* into *multiple linear formats*.

It is a type of versioning, related in spirit to the "track changes" feature in Microsoft Word or even Git, but the goal is to enable parallel documents to exist in relation to one another. Git supports something along these lines through branches, but branches are largely secondary to the linear progression of commits. Other attempts at document versioning for writers, such as Microsoft Word's "track changes" feature, Mac OS X's Time Machine, and Draft do allow easy historical versioning for written material, but they do not provide simultaneous lateral versioning.

The syntax strives to be **simple and self evident**, because it began as an attempt to store software documentation and build it for audiences of different technical skill levels, and it seemed absurd for documentation to have its own documentation. Ideally you should be able to use it without referring back to this page much, if at all.

But, well, here we are. Just in case.

# What **isn't** this?

The build script is nothing special, so Multiverse JSON barely qualifies as software; rather, it is a **set of conventions** (arguably a **specification**) for storing written content in small logical data chunks which allow adaptive output. It is largely agnostic to the actual data format and could be easily reimplemented with alternate storage mechanisms; the relationships are more important than the JSON file.

# Document Structure

The JSON file should contain keys named "metadata" and "root."

## Metadata

This section must contain keys for "instructions" and "versions." You may also add your own arbitrary metadata.

### Instructions

This is a string which contains compilation instructions. Users should feel free to adjust the message, but compiled final products should always include an error message that explains to the reader how to generate alternate versions. (It's OK to hide or remove this message if the context requires it, just make sure to include it in the build.) **This field is required.**

### Versions

This is a hashmap which contains a series of named arrays. The arrays in turn contain strings, some of which are almost certainly going to be references (see below), but literal strings can also be interwoven. **This field is required.**

The versions hashmap **must always contain a key called "default"** which gives the compiler a linear order in which to assemble the nonlinear content blocks by listing literal strings and reference strings in an ordered array. Other alternate build versions may be described similarly, and their keys can be freely, simply, and semantically named.

## Additional Fields

Other fields are allowed in the metadata section. However, in the interest of treating this JSON file like an editorial project, reserved field names are not prefixed or namespaced, and you may find that a custom metadata field name is reserved in a future compiler release.

Here's a JSON document with a valid metadata section. (There's no content root yet, obviously.)

```json
{
  "metadata": {
    "project": "demo",
    "updated": "2015-05-27",
    "versions": {
      "default": [
        "introduction"
        "overview",
        "point_1_explanation",
        "point_1_examples",
        "point_2_explanation",
        "point_3_explanation"
      ]
    }
  }
}
```

# Content Root

This is the content dump. It should contain named keys, one for each logical unit of written content.

## Content Block

What exactly consists a "logical unit" of content is up to you, it could be as large as an entire document or as small as an individual character. Neither of those is likely to be useful, though. There's likely a happy medium – paragraphs, pages, chapters, sections. It's up to you.

## Title

In general, Multiverse JSON prefers to separate section titles and the content filed under them. This should be a string value. It is not required.

## Content

The "content" key is **required**, and should always contain an array containing strings and/or HTML tags which can be glued together to create the compiled editorial for that block – for example, a series of paragraphs. (An array is used to retain readability of the JSON file, since JSON doesn't allow whitespace.)

An array must always be used, even in cases where there is only one item in the content section, so that the compiler or other clients trying to read the JSON can always simply iterate over the array.

The HTML used in this section needs to be minimal, and very strictly structural. It's probably a good idea to include smaller-scope structural markup tags like p and li since they very specifically dictate the immediate structure of the content within the block, but div and h1 aren't relevant in most cases because they are used for larger scale document structure, and the JSON elements can't possibly know what the larger structure of the context in which they are going to be rendered might be.

In other words: dynamic editorial requires a minimalist, purely semantic use of document structure which is sensitive to the need for flexibility.

In the references section below, we'll add some CSS functionality in a moment which can stand in for some of the broader structures lost in this decision. Sit tight.

First, an example with a content block. Note that this is incomplete because some of the required elements of default compilation are undefined; we're just leaving them out in this example for clarity.

```json
{
  "metadata": {
    "project": "demo",
    "updated": "2015-05-27",
    "versions": {
      "default": [
        "introduction"
        "overview",
        "point_1_explanation",
        "point_1_examples",
        "point_2_explanation",
        "point_3_explanation"
      ]
    }
  },
  "root": {
    "introduction": {
      "title": "Introduction",
      "content": [
        "<p>Welcome to our dynamically compiled editorial project!</p>",
        "<p>We're going to use a JSON data file to store our written content. Then we can reassemble it using code.</p>",
        "<p>Once you get it working, it's pretty cool!</p>"
      ]
    }
  }
}
```

## Variants

This key contains an optional hashmap where each named variant key contains a title, contents, and/or variants – that is, an exact, nested clone of the structure used for the primary content block.

Variants are obviously useful for alternate versions of the main contact block – translations, redactions, restatements... this list of possible uses is really endless! They're also useful for cases in which the main content block needs to be further subdivided into subtopics.

Let's add a variant to the above example:

```json
{
  "metadata": {
    "project": "demo",
    "updated": "2015-05-27",
    "versions": {
      "default": [
        "introduction"
        "overview",
        "point_1_explanation",
        "point_1_examples",
        "point_2_explanation",
        "point_3_explanation"
      ]
    }
  },
  "root": {
    "introduction": {
      "title": "Introduction",
      "content": [
        "<p>Welcome to our dynamically compiled editorial project!</p>",
        "<p>We're going to use a JSON data file to store our written content. Then we can reassemble it using code.</p>",
        "<p>Once you get it working, it's pretty cool!</p>"
      ],
      "variants": {
        "i_hate_this": {
          "content": [
            "<p>Whaaaaa?</p>",
            "<p>Why would you ever store written editorial content in a JSON file?</p>",
            "<p>This is dumb.</p>"
          ]
        }
      }
    }
  }
}
```


It is also possible for variants to contain variants, but in those cases you are highly encouraged to rethink the logical structure and titles of your piece, because otherwise you are mandating that all downstream JSON clients build, test, and debug recursive functions for retrieving content, e.g. an inner get_content_variant() running recursively inside an outer get_content_variant() or similar.

In other words: variants are fine, and necessary, but in general a shallower tree structure will be more flexible, easier to read, and less prone to compile errors.

## Undefined Items

It is OK for the main content array to be empty in cases where the focus is on variants, but it should always be present so it's safe for the client application or script to blindly loop without testing the contents first. Technically, it's always safer to include an empty array or string because it makes the compiler less likely to throw an error when a requested item doesn't exist. That said, it detracts from readability. Strike a balance that works for you. (Obviously the best solution is to not request undefined pieces of content for compilation in the first place.)

# References #

So far all we have done is embed HTML in a JSON file, which is only minimal progress. In order for the editorial content to be truly flexible, it needs to be able to repurpose itself, which is to say, certain sections may need to be built out of references to other sections. If we don't solve that problem then we're not really designing dynamic, flexible, repurposable structured writing – we're just encoding the usual text or HTML in a JSON file and will end up rewriting the same material many times with very slight changes.

We solve this problem by designating "refer@" as a reserved keyword at the beginning of strings. If that text appears at the beginning of a string in a content array, that string should instead be interpreted as an instruction to retrieve a piece of text or HTML defined elsewhere in the data file, the precise location of which is described in traditional JavaScript dot notation. The compilation tool or other client renderer should be designed to interpret each of these strings as an instruction to look up the corresponding information and render it just as it would any other regular string.

An example of what this would look like. (Note that this example omits the metadata section for clarity.)

```json
{
  "root": {
      "something_useful": {
          "title": "This is something useful.",
          "content": [
            "Here's some actual content which will be imported with a reference into another part of the document."
          ]
      },
      "references_example": {
          "title": "An Example of References",
          "content": [
              "<h3>This is how references work.</h3>",
              "refer@root.something_useful.title",
              "refer@root.something_useful.content"
          ]
      }
    }
}
```

The use of references also allows for the establishment of default values among a set of variants. The content can be stored in a variant, and called from the content property using a reference.

```json
{
  "root": {
        "set_default_example": {
            "title": "This is how to use references to establish a default value. It will default to greeting the reader in Spanish.",
            "content": "refer@set_default_example.variants.spanish.content",
            "variants": {
                "english": {
                    "title": "greeting",
                    "content": "hello!"
                },
                "spanish": {
                    "title": "greeting",
                    "content": "¡hola!"
                }
            }
        }
    }
}
```

## Reference Attributes

References can be followed by optional recommended CSS selectors which the client or build tool is free to ignore. This is especially useful in conjunction with something like Twitter Bootstrap, which allows styling from CSS classes (e.g. class="h5") to override conflicting DOM tags (e.g. &lt;h5&gt;) – that is, you can make literally any element look like an h5 if you simply add that class to it.

```json
{
    "something_useful": {
        "title": "This is something useful.",
        "content": [
          "Here's some actual content which will be imported with a reference into another part of the document, with additional attributes appended."
        ]
    },
    "references_example": {
        "title": "An Example of References, with attributes",
        "content": [
            "<h3>This is how references work.</h3>",
            "refer@root.something_useful.title #example-heading .title",
            "refer@root.something_useful.content #example-content .body"
        ]
    }
}
```

In most cases it should be possible to use classes and IDs to set up a fairly complex DOM-aware web application, but attributes other than classes and IDs can also be added, albeit without any shorthand, allowing you to set up a complex web application in one rendering pass, including fancier features like data attributes and Angular.js directives. For the sake of JSON readability, you'll probably want to use single quotes around your attribute values rather than escape double quotes.

Here's an example of references which will wrap the content in both CSS selectors and additional attributes.

```json
{
  "root": {
    "something_useful": {
        "title": "This is something useful.",
        "content": [
          "Here's some actual content which will be imported with a reference into another part of the document."
        ]
    },
    "references_example": {
        "title": "An Example of References",
        "content": [
            "<h3>This is how references work.</h3>",
            "refer@root.something_useful.title #example-heading .title data-url='http://www.google.com' ng-click='executeSomeFunction'",
            "refer@root.something_useful.content #example-content .body"
        ]
    }
  }
}
```

Readability and syntactic clarity are major goals for this JSON file, so it is absolutely the responsibility of the renderer or build tool to examine the first character of the additional attribute and allow the shorthand. Don't skip this when writing your renderer! It will help your users, readers, and developers a lot! Additional attributes around references should in most cases be rendered with a span tag instead of a div, so as to not introduce any unexpected line breaks. If you do need a block level element, it should be provided by the renderer, build tool, styling, or default order markup, not introduced by the use of reference syntax in the data file. **The use of limited scope structural markup, most notably p tags, will limit the visibility of unwanted inline rendering caused by using spans instead of divs for reference attribute shorthand.**

Note the slight difference here between the compilation tool and other client applications: the compilation tool *should support the attribute shorthand* to encourage syntactic clarity when the data file is being written. However, other client applications beyond the compilation tool are *still free to ignore those attributes* because the data source can't reasonably expect to mandate implementation for every possible use case.

Additional attributes need only need to be inserted around references, not the original location of the content item, because the original location of the content item is just an array of strings, so it's already easy to add attributes directly without the need for a complicated syntax parser.

## Reference Recursion

References are resolved through string analysis, so the simplest way to write a renderer or build tool that supports them is with a recursive function that calls itself again when it detects a reference which needs to be resolved. If you'd like to cleanly separate your retrieval of content objects and their rendering into HTML strings, feel free to do some heavy handed array splicing. Consider, though, that this specification technically allows for infinite redirecting of content using these references, for which a truly recursive function is actually probably a more robust solution, albeit possibly a bit off-putting architecturally.

For maximum flexibility, references point specifically to title and content, not to the parent key representing the overall piece of content, because otherwise it would be unclear whether the compiled references should include the title as a section header.

In the specific context of this schema, a reference can also be used to compile a number of variants representing subsections into a single longer passage which can be printed in a complete content dump.

There's an important compromise happening here: documents are by their nature structured and hierarchical, but reflecting that in the data also limits its future flexibility. As a middle ground, references allow the quick and flexible insertion of CSS selectors which can be used to make sure visual presentation conveys a useful hierarchy of concepts and information even if the document DOM tree is flatter than the styling might suggest. And since the content arrays just glue together arbitrary strings, you can always string together a set of references to the original information and insert div tags and other DOM hierarchies as desired in cases where a visual hierarchy alone isn't sufficient.

# Best Practices

It's important to explain this system system within the finished content build; again, the goal is to prevent users from ever having to view this page. This is tricky, because we need this to a) validate b) be readable in unrendered JSON/code form c) be readable after rendering and d) not require a rendering/build stage. These are mutually exclusive, especially when you consider that JSON requires literal newlines. So instead, we'll punt on this problem entirely, and write detailed instructions as plaintext comments in the Python source code, then leave clues to the user instructing them to open that file if they want to read the detailed compilation instructions.

Specifically, best practices include:

1. The Python build script should include *extremely detailed* instructions in comments located at the *very top of the file* which explain the exact terminal commands used to update the JSON file and run the build task. Remember that these instructions may one day be read by someone who just wants to understand how to use the application, and has never touched Python, JSON, nor the command line. Be extremely verbose.

1. The data file's "metadata" key should also contain a property called "instructions" which briefly explains how to open the compilation script and find the more detailed instructions in the Python script comments. This should just be a brief pointer, again because JSON doesn't support newlines, so readability of multiline content will always be compromised either in JSON or in the rendered HTML. Don't overthink this one.

1. The instructions property in the content object should be appended by the build script in readable form to the finished HTML build. Be sure to give it a class so it can be easily hidden or removed by CSS or JavaScript downstream.

1. In many cases it may be desirable to avoid shipping pre-built HTML. In these cases we should instead ship a blank index.html or README.md or similar which contains only the "instructions" property from the JSON object's metadata key. More technical users can be trusted to run the builds themselves if the instructions written at the top of the build script are friendly enough.

1. The build script should end successful builds by printing a message to the terminal window which includes the specific names of the input and output files and tells users specifically where to read their newly built or rebuilt document.
