use aocrust::io::from_file;
use std::collections::HashSet;
use std::collections::VecDeque;

fn find_sequence_index(s: &str, len: usize) -> Option<usize> {
    let mut chars: VecDeque<char> = VecDeque::new();
    for (i, c) in s.chars().enumerate() {
        chars.push_front(c);
        if chars.len() > len {
            chars.pop_back();
        }
        let set = chars.iter().collect::<HashSet<&char>>();
        if set.len() == len {
            return Some(i + 1);
        }
    }

    None
}

fn solve1(filename: &str) -> u64 {
    find_sequence_index(from_file(filename).trim(), 4).unwrap() as u64
}

fn solve2(filename: &str) -> u64 {
    find_sequence_index(from_file(filename).trim(), 14).unwrap() as u64
}

fn main() {
    println!("{}", solve1("input.txt"));
    println!("{}", solve2("input.txt"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(
            find_sequence_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4).unwrap(),
            7
        );
        assert_eq!(
            find_sequence_index("bvwbjplbgvbhsrlpgdmjqwftvncz", 4).unwrap(),
            5
        );
        assert_eq!(
            find_sequence_index("nppdvjthqldpwncqszvftbrmjlhg", 4).unwrap(),
            6
        );
        assert_eq!(
            find_sequence_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4).unwrap(),
            10
        );
        assert_eq!(
            find_sequence_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4).unwrap(),
            11
        );
    }

    #[test]
    fn test_part2() {
        assert_eq!(
            find_sequence_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14).unwrap(),
            19
        );
        assert_eq!(
            find_sequence_index("bvwbjplbgvbhsrlpgdmjqwftvncz", 14).unwrap(),
            23
        );
        assert_eq!(
            find_sequence_index("nppdvjthqldpwncqszvftbrmjlhg", 14).unwrap(),
            23
        );
        assert_eq!(
            find_sequence_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14).unwrap(),
            29
        );
        assert_eq!(
            find_sequence_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14).unwrap(),
            26
        );
    }
}
