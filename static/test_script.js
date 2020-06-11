describe ("Testing functions for exoplanet app", () => {

    it ("should submit new favorite planet to user list and receive response with addPlanet", async function() {
        resp = await addPlanet("testuser", 1, "11 Com b");

        expect(resp.data.new_favorite.list).toEqual("testplanets");
        expect(resp.data.new_favorite.planet).toEqual("11 Com b");
    })
})