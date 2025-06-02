import argparse

from game import Game

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Tunnel Evacuation Simulation",
        description='Project created for AGH "Agent Systems" course. Simulates the behaviour of agents evacuating from the road tunnel.',
        epilog="Created by @kubijaku and @MarcinZ20",
    )

    parser.add_argument("-f", "--File", required=True, help="Simulation file")
    parser.add_argument("-o", "--Output", help="Output file path")

    args = parser.parse_args()

    game = Game(args.File, args.Output)

    while True:
        game.new_instance()
        game.run()
