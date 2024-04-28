# Project demonstration

## General flow
```mermaid
flowchart
    A(Home) --Enter playlist--> I(Streamlit app)
    A --Find out--> B(Input)
    
    B --Choose  diagnosis-->D(Diagnose)
    B --Customize preference--> C(Fetch)

    D --> E
    C --> E(Preview music)
    E --> F(Open on Spotify)
    F --Show receipt--> G(Receipt)
    
    G --Download--> J(PNG)
    G --Send email--> H(Open Gmail)
    G --New diagnosis-->A
```

## Allocation
**Ashton**: 
- Overview of the project. Indicate this is a `music taste analysis and recommendation` system
- Start from home introduce options
- Overview of input page

**Hilmy**:
- Execute `diagnosis`
- Overview of results: analysis, artists, songs, playlists
- Preview song on page
- Not mention open on Spotify yet

**Adam**:
- Demonstrate `receipt` component
- Download receipt
- Send email

**Quan**:
- Re-execute with customized preference
- Play music on Spotify 