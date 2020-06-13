describe ("Testing functions for exoplanet app", () => {

    // There must be a list added to user's list for testing
    it ("should submit new favorite planet to user list and receive response with addPlanet", async function() {
        const listID =parseInt($('.listIDs')[0].value);
        const listName = $('.listIDs')[0].text;
        const resp = await addFavorite(listID, ["testPlanet"]);
        
        expect(resp.list).toEqual(listName);
        expect(resp.planets).toEqual(["testPlanet"]);
    })

    // There must be a list added to user's list for testing
    it ("should submit multiple favorite planets to user list and receive response with addPlanet", async function() {
        const listID =parseInt($('.listIDs')[0].value);
        const listName = $('.listIDs')[0].text;
        resp = await addFavorite(listID, ["testPlanet1", "testPlanet2"]);

        expect(resp.list).toEqual(listName);
        expect(resp.planets).toEqual(["testPlanet1", "testPlanet2"]);
    })

    it ("should return total number of result pages with getTotalPages", () => {
        expect(getTotalPages(4164)).toEqual(42);
        expect(getTotalPages(9)).toEqual(1);
        expect(getTotalPages(101)).toEqual(2);
    })

    it ("should return first page link of set on page with getPageStart", () => {
        expect(getPageStart(4164, 8)).toEqual(1);
        expect(getPageStart(9, 1)).toEqual(1);
        expect(getPageStart(1000,11)).toEqual(10);
    })
    
    it ("should return last page link of set on page with getPageEnd", () => {
        expect(getPageEnd(4164, 1)).toEqual(9);
        expect(getPageEnd(4164, 10)).toEqual(19);
        expect(getPageEnd(9,1)).toEqual(9);
    })

    it ("should return start of next set of 10 pages with getNextPageSet", () => {
        expect(getNextPageSet(40, 29)).toEqual(30);
        expect(getNextPageSet(9, 9)).toBeUndefined();
        expect(getNextPageSet(12, 9)).toEqual(10);
        expect(getNextPageSet(40, 39)).toBe(40);
    })
    
    it ("should return start of previous set of 10 pages with getPreviousPageSet", () => {
        expect(getPreviousPageSet(20)).toEqual(1);        
        expect(getPreviousPageSet(10)).toBeUndefined();        
        expect(getPreviousPageSet(40)).toEqual(20);        
    })
})