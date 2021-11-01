use futures::future::join_all;
use reqwest::Client;
use rusqlite::Connection;
use scraper::element_ref::ElementRef;
use scraper::{Html, Selector};
use std::vec::Vec;
use tokio;

#[derive(Debug, Clone)]
pub struct Drawing {
    DrawingID: i64,
    Date: String,
    Position: i64,
    Drawing: String,
}

async fn get_data(client: &Client, year: usize, connection: &Connection) {
    println!("==>> {}", year);
    let url = format!(
        "https://fwnk.cw/wega-di-number-korsou/archivo-wega-di-number/?show_year={}",
        year
    );
    println!("Getting page : {}", &url);
    let body = client.get(&url).send().await.unwrap().text().await.unwrap();
    let html = Html::parse_document(&body);
    let tr_selector = Selector::parse("tr:nth-of-type(2n)").unwrap();

    for tr in html.select(&tr_selector) {
        let td_selector = Selector::parse("td").unwrap();
        let td_select: Vec<ElementRef> = tr.select(&td_selector).collect();

        if td_select.len() == 5 {
            let date: String = td_select[0].text().collect();
            if date.len() == 10 {
                let number1: String = td_select[1].text().collect();
                let number2: String = td_select[2].text().collect();
                let number3: String = td_select[3].text().collect();
                let day: String = date.chars().skip(8).take(2).collect();
                let month: String = date.chars().skip(5).take(2).collect();
                let year: String = date.chars().take(4).collect();
                let date_format = format!("{}{}{}", day, month, year);
                let query_str: String = String::from("SELECT * FROM Drawing WHERE Date = ?");
                let mut drawings_prepare = connection.prepare(&query_str).unwrap();
                let exists = drawings_prepare.exists([&date_format]).unwrap();

                if !exists {
                    println!("Creating Entry for {}", &date_format);
                    connection
                        .execute(
                            "INSERT INTO Drawing (Date,Position,Drawing) Values(?, ?, ?)",
                            [&date_format, "1", &number1],
                        )
                        .unwrap();
                    connection
                        .execute(
                            "INSERT INTO Drawing (Date,Position,Drawing) Values(?, ?, ?)",
                            [&date_format, "2", &number2],
                        )
                        .unwrap();
                    connection
                        .execute(
                            "INSERT INTO Drawing (Date,Position,Drawing) Values(?, ?, ?)",
                            [&date_format, "3", &number3],
                        )
                        .unwrap();
                }
            }
        }
    }

    println!("{} Finnished", &url);
}

#[tokio::main]
async fn main() {
    let connection = Connection::open("./database/basedb.db").unwrap();
    const START_YEAR: usize = 2014;
    const END_YEAR: usize = 2021;
    let client = Client::new();
    let year_array: [usize; END_YEAR - START_YEAR + 1] = [0; END_YEAR - START_YEAR + 1];
    let mut year_vec = Vec::new();

    for (index, year) in year_array.iter().enumerate() {
        year_vec.push(get_data(&client, index + START_YEAR, &connection));
    }
    
    join_all(year_vec).await;
}
