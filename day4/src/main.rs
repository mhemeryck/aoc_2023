use std::fs::read_to_string;

const FILENAME: &str = "input.txt";

fn parse_numbers(number_str: &str) -> Vec<u64> {
    number_str
        .split(" ")
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .map(|s| s.parse().unwrap())
        .collect()
}

fn main() {
    let fh = read_to_string(FILENAME).unwrap();

    let mut result = 0;
    for line in fh.lines() {
        let v: Vec<&str> = line.split(":").collect();
        let (_game_str_id, payload) = (v[0], v[1]);

        let v: Vec<&str> = payload.split("|").collect();
        let (winning_str, actual_str) = (v[0], v[1]);

        let winning = parse_numbers(winning_str);
        let actual = parse_numbers(actual_str);

        let line_count: u64 = winning.iter().map(|w| actual.contains(&w) as u64).sum();
        if line_count > 0 {
            result += 1 << (line_count - 1)
        }
    }
    println!("{:?}", result);
}
