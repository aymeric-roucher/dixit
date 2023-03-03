# What is Dixit ❔

> Disclaimer: we will quote historical people, so we give credits. ["Render unto Caesar"](https://en.wikipedia.org/wiki/Render_unto_Caesar) as they say.

Dixit is an online app that boost your confidence: when you have a smart idea, it lets you see which historical people came upon this same smart idea. "Great minds think alike", as they say 🧐.

But the truth is, these particular great minds probably formulated the idea way better than you could. So why not quote them directly, and ["stand on the shoulders of [these] giants"](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants)?

Dixit lets you type in your poorly formulated, rough-edged idea, and through a ["tremendous"](https://www.theatlantic.com/magazine/archive/2018/03/how-to-talk-trump/550934/) ["AI powered semantic search"](https://www.reddit.com/r/consulting/comments/6x8a34/have_any_of_you_snakeoil_salesmen_ever_actually/), it retrieves a quote with a similar idea from its database of historical quotations.


# How it works

["A good sketch is worth a long speech"](https://en.wikipedia.org/wiki/Napoleon), so here's a graph of the system design.

```mermaid
graph TD
    subgraph GITHUB REPO
        searchbar_page(<font color=black>Index: Search page<br>/User sentence/)
        author_page(<font color=black>Specific Author page)
        quotes_table{<font color=black>fa:fa-database Quotes<br>table<br>4 mo}
        faiss_index{<font color=black>fa:fa-search FAISS Index<br>36 mo}
        search_request[Embedded sentence]
        searchbar_page-.LLM embedding-.->search_request
        quotes_table-.Returns closest quotes-.->searchbar_page
        search_request-.Similarity search-.->faiss_index
        faiss_index -.Query quotes at selected indexes-.-> quotes_table
        author_page --Gets author quotes--> quotes_table
    end

    subgraph POSTGRESQL DATABASE
        authors_table{<font color=black>fa:fa-database Authors table}
    end

    %% Notice that no text in shape are added here instead that is appended further down
    author_page--Get author data-->authors_table

    classDef green fill:#9f6,stroke:#333,stroke-width:3px;
    classDef orange fill:#f96,stroke:#333,stroke-width:3px;
    class author_page,searchbar_page green
    class quotes_table,faiss_index,authors_table orange
```

# How it does not work

For now, it still has a limited database of quotes, so searching for the idea "NFT is a huge pile of scam" will return only remote ideas. But hey, we can't make coffee for you either.

# 