import XCTest

final class NativeFlowTests: XCTestCase {
    let app = XCUIApplication(bundleIdentifier: "org.reactjs.native.example.ShopDiscover")

    func capture(_ name: String) {
        let attachment = XCTAttachment(screenshot: app.screenshot())
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    func enter(_ text: String, into field: XCUIElement) {
        // Let each controlled React Native input update settle before the next
        // synthesized key. A single rapid XCTest batch lost later characters.
        var expected = ""
        for character in text {
            field.typeText(String(character))
            expected += String(character)
            let settled = NSPredicate(format: "value == %@", expected)
            expectation(for: settled, evaluatedWith: field)
            waitForExpectations(timeout: 5)
        }
    }

    func testSearchFiltersDetailsAndReturn() {
        continueAfterFailure = false
        app.launch()
        let search = app.textFields["Search products"]
        XCTAssertTrue(search.waitForExistence(timeout: 30), app.debugDescription)
        capture("ios-online")
        app.buttons["Filters"].tap()
        XCTAssertTrue(app.buttons["Hide filters"].waitForExistence(timeout: 5), app.debugDescription)
        app.buttons["Hide filters"].tap()
        search.coordinate(withNormalizedOffset: CGVector(dx: 0.2, dy: 0.5)).tap()
        XCTAssertTrue(app.keyboards.firstMatch.waitForExistence(timeout: 5), app.debugDescription)
        enter("phone", into: search)
        search.typeText("\n")
        XCTAssertTrue(app.staticTexts["16 of 194 products"].waitForExistence(timeout: 10))
        capture("ios-phone-search")

        app.buttons["Filters"].tap()
        app.switches["In stock only"].tap()
        XCTAssertTrue(app.staticTexts["15 of 194 products"].waitForExistence(timeout: 5))
        let maxPrice = app.textFields["Maximum price"]
        maxPrice.tap()
        enter("500", into: maxPrice)
        // Tap the non-input heading to dismiss decimal-pad via the Apply action.
        app.buttons["Apply price range"].tap()
        XCTAssertTrue(app.staticTexts["12 of 194 products"].waitForExistence(timeout: 5))
        app.buttons["Hide filters"].tap()
        app.swipeUp()

        let cards = app.buttons.matching(NSPredicate(format: "label BEGINSWITH %@", "View details for "))
        let visibleCards = cards.allElementsBoundByIndex.filter { $0.isHittable }
        XCTAssertFalse(visibleCards.isEmpty)
        let card = visibleCards[0]
        let label = card.label
        let before = card.frame
        capture("ios-filtered-scrolled")
        card.tap()
        XCTAssertTrue(app.navigationBars["Product details"].waitForExistence(timeout: 5))
        capture("ios-details")
        app.navigationBars.buttons.element(boundBy: 0).tap()
        XCTAssertTrue(search.waitForExistence(timeout: 5))
        XCTAssertEqual(search.value as? String, "phone")
        XCTAssertTrue(app.staticTexts["12 of 194 products"].exists)
        let returned = app.buttons[label]
        XCTAssertTrue(returned.isHittable)
        XCTAssertEqual(returned.frame.minY, before.minY, accuracy: 3)
        capture("ios-back-preserved")

        app.buttons["Filters"].tap()
        XCTAssertEqual(app.textFields["Maximum price"].value as? String, "500")
        app.buttons["Reset all"].tap()
        XCTAssertTrue(app.staticTexts["194 of 194 products"].waitForExistence(timeout: 5))
        capture("ios-reset")
    }

    func testSwipeBackPreservesBrowsingPosition() {
        continueAfterFailure = false
        app.launch()
        XCTAssertTrue(app.textFields["Search products"].waitForExistence(timeout: 30))
        app.swipeUp()
        let cards = app.buttons.matching(NSPredicate(format: "label BEGINSWITH %@", "View details for "))
        let card = cards.allElementsBoundByIndex.first { $0.isHittable }!
        let label = card.label
        let before = card.frame
        card.tap()
        XCTAssertTrue(app.navigationBars["Product details"].waitForExistence(timeout: 5))
        let edge = app.coordinate(withNormalizedOffset: CGVector(dx: 0.01, dy: 0.5))
        let end = app.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5))
        edge.press(forDuration: 0.1, thenDragTo: end)
        XCTAssertTrue(app.textFields["Search products"].waitForExistence(timeout: 5))
        let returned = app.buttons[label]
        XCTAssertTrue(returned.isHittable)
        XCTAssertEqual(returned.frame.minY, before.minY, accuracy: 3)
        capture("ios-swipe-back-preserved")
    }
}
