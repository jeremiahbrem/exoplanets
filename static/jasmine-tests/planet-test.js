describe("testing planet page functions", () => {
    
    it ("should return rgb value from getRGBFromBV", () => {
        expect(getRGBFromBV(3)).toEqual("rgb(255,112.52779799999999,0)");
        expect(getRGBFromBV(-0.4)).toEqual("rgb(68.846173,68.846173,255)");
        expect(getRGBFromBV(0)).toEqual("rgb(158.076933,158.076933,255)");
    })

    it ("should return width values object from comparePlanetSize", () => {
        expect(comparePlanetSize(1)).toEqual({earthWidth: 50, exoWidth: 50});
        expect(comparePlanetSize(0.1)).toEqual({earthWidth: 50, exoWidth: 5});
        expect(comparePlanetSize(157)).toEqual({earthWidth: 1.910828025477707, exoWidth: 300});
    })

    it ("should return B-V index value from spectral type with getBVFromSpectral", () => {
        expect(getBVFromSpectral("B")).toEqual(-0.3);
        expect(getBVFromSpectral("B8")).toEqual(-0.08399999999999999);
        expect(getBVFromSpectral("A")).toEqual(-0.02);
        expect(getBVFromSpectral("A3")).toEqual(0.076);
        expect(getBVFromSpectral("F")).toEqual(0.3);
        expect(getBVFromSpectral("F0")).toEqual(0.3);
        expect(getBVFromSpectral("G")).toEqual(0.58);
        expect(getBVFromSpectral("G1")).toEqual(0.603);
        expect(getBVFromSpectral("K")).toEqual(0.81);
        expect(getBVFromSpectral("K9")).toEqual(1.341);
        expect(getBVFromSpectral("M")).toEqual(1.4);
        expect(getBVFromSpectral("M5")).toEqual(1.7);
    })

    it ("should return B-V index value from temperature with getBVFromTemp", () => {
        expect(getBVFromTemp(30000)).toEqual(-0.3);
        expect(getBVFromTemp(58000)).toEqual(-0.6740722414646215);
        expect(getBVFromTemp(2300)).toEqual(2.5);
    })    

    it ("should return scale sizes for stars from given radius with compareStarSize", () => {
        expect(compareStarSize(1)).toEqual({sunScale: 0.5, exoScale: 0.5});
        expect(compareStarSize(0.05)).toEqual({sunScale: 0.5, exoScale: 0.025});
        expect(compareStarSize(45)).toEqual({sunScale: 0.011111111111111112, exoScale: 0.5});
    })    
    
    it ("should return width sizes for planets from given radius with comparePlanetSize", () => {
        expect(compareStarSize(1)).toEqual({sunScale: 0.5, exoScale: 0.5});
        expect(compareStarSize(0.05)).toEqual({sunScale: 0.5, exoScale: 0.025});
        expect(compareStarSize(45)).toEqual({sunScale: 0.011111111111111112, exoScale: 0.5});
    })    
})