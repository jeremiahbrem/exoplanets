describe("testing functions for adding, deleting favorites", () => {
    
    it ("should submit new favorite planet to user list and receive response with addFavorite", async function() {
        const listID =parseInt($('.listIDs')[0].value);
        const listName = $('.listIDs')[0].text;
        const resp = await addFavorites(listID, ["testPlanet"]);
        
        expect(resp.list).toEqual(listName);
        expect(resp.planets).toEqual(["testPlanet"]);
    })
    
    it ("should submit multiple favorite planets to user list and receive response with addFavorite", async function() {
        const listID =parseInt($('.listIDs')[0].value);
        const listName = $('.listIDs')[0].text;
        resp = await addFavorites(listID, ["testPlanet1", "testPlanet2"]);
    
        expect(resp.list).toEqual(listName);
        expect(resp.planets).toEqual(["testPlanet1", "testPlanet2"]);
    })

    // it ("should select planet results and add to user list", async function() {
    //     $('')
    // })
})