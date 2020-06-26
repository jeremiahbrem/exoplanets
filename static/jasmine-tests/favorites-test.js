describe("testing Favorites class functions", () => {
    
    const $listID =parseInt($('#list-id').val());
    const $listName = $('#list-name').text();
    const $userID = $('#user-id').val();

    it ("should submit new favorite planet to user list and receive response with addFavorite", async function() {
        const resp = await Favorites.addFavorites($listID, ["testPlanet1"]);
      
        expect(resp.data.messages).toContain(`testPlanet1 added to ${$listName}`);

        await Favorites.deleteFavorite($listID, "testPlanet1");
    })
    
    it ("should submit multiple favorite planets to user list and receive response with addFavorite", async function() {
        const resp = await Favorites.addFavorites($listID, ["testPlanet2", "testPlanet3"]);
        
        expect(resp.data.messages).toContain(`testPlanet2 added to ${$listName}`);
        expect(resp.data.messages).toContain(`testPlanet3 added to ${$listName}`);

        await Favorites.deleteFavorite($listID, "testPlanet2");
        await Favorites.deleteFavorite($listID, "testPlanet3");
    })

    it ("should receive duplicate add response if favorites already exists in list with addFavorite", async function() {
        await Favorites.addFavorites($listID, ["testPlanet4"]);
        const resp = await Favorites.addFavorites($listID, ["testPlanet4"]);

        expect(resp.data.messages).toContain(`testPlanet4 already exists in ${$listName}`);
    })

    it ("should delete favorites from page and from database with deleteFavorite", async function() {
        const addResp = await Favorites.addFavorites($listID, ["testPlanet5"]);
        const deleteResp = await Favorites.deleteFavorite($listID, "testPlanet5")
        expect(deleteResp).toEqual("testPlanet5 deleted from list.")
    })

    it ("should create favorites list and get response from back-end with createList", async function() {
        const resp = await Favorites.createList("myList");
        console.log(resp)
        expect(resp.list_id).toBeInstanceOf(Number);
        expect(resp.list_name).toEqual("myList")
    })
})