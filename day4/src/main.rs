use std::{collections::HashMap, fs::read_to_string};

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
    let mut line_counts: HashMap<u64, u64> = HashMap::new();
    for line in fh.lines() {
        let v: Vec<&str> = line.split(":").collect();
        let (game_str_id, payload) = (v[0], v[1]);

        let v: Vec<&str> = game_str_id.split(char::is_whitespace).collect();
        let game_id: u64 = v[v.len() - 1].parse().unwrap();

        let v: Vec<&str> = payload.split("|").collect();
        let (winning_str, actual_str) = (v[0], v[1]);

        let winning = parse_numbers(winning_str);
        let actual = parse_numbers(actual_str);

        let line_count: u64 = winning.iter().map(|w| actual.contains(&w) as u64).sum();
        if line_count > 0 {
            result += 1 << (line_count - 1)
        }
        line_counts.insert(game_id, line_count);
    }
    println!("Result part 1: {:?}", result);

    println!("Line counts: {:?}", line_counts);

    let max_game_id = line_counts.keys().max().unwrap();
    let mut counter: HashMap<u64, u64> = HashMap::with_capacity((max_game_id - 1) as usize);
    // Init by one to begin with
    for line_count in counter.values_mut() {
        *line_count = 1;
    }

    for (game_id, line_count) in counter {
        let fro = game_id + 1;
        let to = game_id + line_count + 1;

        for next_id in fro..to {
            *counter.get_mut(&next_id).unwrap() += line_counts.get(&game_id).unwrap();
        }
    }
}
