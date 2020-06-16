describe("testing Favorites class functions", () => {
    
    const $listID =parseInt($('#list-id').val());
    const $listName = $('#list-name').text();

    it ("should submit new favorite planet to user list and receive response with addFavorite", async function() {
        const resp = await Favorites.addFavorites($listID, ["testPlanet1"]);
        expect(resp.list).toEqual($listName);
        expect(resp.planets).toEqual(["testPlanet1"]);

        await Favorites.deleteFavorite($listID, "testPlanet1");
    })
    
    it ("should submit multiple favorite planets to user list and receive response with addFavorite", async function() {
        const resp = await Favorites.addFavorites($listID, ["testPlanet2", "testPlanet3"]);
        expect(resp.list).toEqual($listName);
        expect(resp.planets).toContain("testPlanet2");
        expect(resp.planets).toContain("testPlanet3");

        await Favorites.deleteFavorite($listID, "testPlanet2");
        await Favorites.deleteFavorite($listID, "testPlanet3");
    })

    it ("should delete favorites from page and from database", async function() {
        const addResp = await Favorites.addFavorites($listID, ["testPlanet4"]);
        const deleteResp = await Favorites.deleteFavorite($listID, "testPlanet4")
        expect(deleteResp).toEqual("testPlanet4 deleted from list.")
    })
})